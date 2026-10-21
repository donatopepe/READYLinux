#!/usr/bin/env python3
"""Record a read-only Yocto host preflight as auditable JSON evidence.

The recorder refuses to invent build results: it only captures the preflight
report plus provenance (UTC time, READY Linux commit) and states the scope.
Exit codes: 0 written, 3 preflight not ready, 4 output exists without --force,
5 preflight report contradicts its own "ready" verdict.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCHEMA_VERSION = 1
SCOPE = (
    "preflight-only: no BitBake metadata parse, no image build, no QEMU boot; "
    "this record is not build evidence"
)


RECORD_KEYS = ("schema_version", "recorded_utc", "readylinux_commit", "scope", "preflight_command", "preflight_exit_code", "preflight")
REPORT_KEYS = ("schema_version", "os", "arch", "cpus", "required", "missing_required", "optional", "builddir", "verdict")
VERDICTS = ("ready", "incomplete", "not-a-linux-host")


def validate_record(record: dict) -> list[str]:
    """Return structural problems found in a stored record (empty when valid)."""
    problems: list[str] = []
    if not isinstance(record, dict):
        return ["record is not a JSON object"]
    for key in RECORD_KEYS:
        if key not in record:
            problems.append(f"missing top-level key: {key}")
    extra = set(record) - set(RECORD_KEYS)
    if extra:
        problems.append(f"unexpected top-level keys: {', '.join(sorted(extra))}")
    if record.get("schema_version") != SCHEMA_VERSION:
        problems.append("schema_version must be 1")
    recorded_utc = record.get("recorded_utc", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(recorded_utc)):
        problems.append("recorded_utc must look like 2026-10-20T00:00:00Z")
    else:
        try:
            parsed_utc = datetime.strptime(recorded_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            problems.append("recorded_utc is not a valid calendar timestamp")
        else:
            if parsed_utc > datetime.now(timezone.utc) + timedelta(minutes=5):
                problems.append("recorded_utc is in the future")
    if not re.fullmatch(r"[0-9a-f]{40}", str(record.get("readylinux_commit", ""))):
        problems.append("readylinux_commit must be a 40-character lowercase hex commit")
    if not isinstance(record.get("scope"), str) or "not build evidence" not in record["scope"].lower():
        problems.append("scope must state that the record is not build evidence")
    if isinstance(record.get("preflight_exit_code"), bool) or record.get("preflight_exit_code") != 0:
        problems.append("preflight_exit_code must be integer 0")

    report = record.get("preflight")
    if not isinstance(report, dict):
        return problems + ["preflight must be a JSON object"]
    for key in REPORT_KEYS:
        if key not in report:
            problems.append(f"missing preflight key: {key}")
    if report.get("verdict") not in VERDICTS:
        problems.append(f"preflight.verdict must be one of {', '.join(VERDICTS)}")
    if report.get("verdict") != "ready":
        problems.append("preflight.verdict must be ready for a recorded host-evidence artifact")
    os_block = report.get("os")
    if not isinstance(os_block, dict) or set(os_block) != {"name", "id", "version_id"}:
        problems.append("preflight.os must contain exactly name, id and version_id")
    elif any(not isinstance(os_block[key], str) or not os_block[key].strip() for key in ("name", "id")):
        problems.append("preflight.os name and id must be non-empty strings")
    if isinstance(report.get("cpus"), bool) or not isinstance(report.get("cpus"), int) or report["cpus"] < 0:
        problems.append("preflight.cpus must be a non-negative integer, not a boolean")
    version_id = os_block.get("version_id") if isinstance(os_block, dict) else None
    if version_id is not None and (not isinstance(version_id, str) or not version_id.strip()):
        problems.append("preflight.os.version_id must be null or a non-empty string")
    packages = report.get("packages")
    if not isinstance(packages, dict) or not all(
        isinstance(name, str) and name.strip() and (value is None or isinstance(value, str) and value.strip())
        for name, value in packages.items()
    ):
        problems.append("preflight.packages must map non-empty package names to non-empty versions or null")
    if not isinstance(report.get("arch"), str) or not report["arch"].strip():
        problems.append("preflight.arch must be a non-empty string")
    for mapping in ("required", "optional"):
        block = report.get(mapping)
        if not isinstance(block, dict) or not all(
            isinstance(name, str) and name.strip() and isinstance(value, bool)
            for name, value in block.items()
        ):
            problems.append(f"preflight.{mapping} must map non-empty command names to booleans")
    missing_required = report.get("missing_required")
    if not isinstance(missing_required, list) or not all(isinstance(item, str) and item.strip() for item in missing_required):
        problems.append("preflight.missing_required must be a list of non-empty command names")
    elif len(missing_required) != len(set(missing_required)):
        problems.append("preflight.missing_required must not contain duplicate command names")
    required_tools = report.get("required")
    if isinstance(required_tools, dict) and isinstance(missing_required, list):
        derived_missing = sorted(name for name, available in required_tools.items() if not available)
        if sorted(missing_required) != derived_missing:
            problems.append("preflight.missing_required does not match false entries in preflight.required")
    builddir = report.get("builddir")
    if not isinstance(builddir, dict) or set(builddir) != {"set", "path"}:
        problems.append("preflight.builddir must contain exactly set and path")
    elif not isinstance(builddir["set"], bool):
        problems.append("preflight.builddir.set must be a boolean")
    elif builddir["set"] and (not isinstance(builddir["path"], str) or not builddir["path"].strip()):
        problems.append("preflight.builddir.path must be a non-empty string when set is true")
    elif not builddir["set"] and builddir["path"] is not None:
        problems.append("preflight.builddir.path must be null when set is false")
    contradiction = inconsistent_ready_report(report)
    if contradiction is not None:
        problems.append(contradiction)
    return problems


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record a read-only Yocto host preflight as JSON.")
    parser.add_argument("output", nargs="?", help="path of the JSON record to write")
    parser.add_argument(
        "--check",
        metavar="PATH",
        help="validate an existing record instead of writing a new one",
    )
    parser.add_argument(
        "--preflight-script",
        default=None,
        help="path to check-yocto-host.sh (default: sibling of this script)",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="repository whose HEAD is recorded (default: git toplevel of the preflight script)",
    )
    parser.add_argument("--force", action="store_true", help="overwrite an existing record")
    return parser


def preflight_argv(script: Path) -> list[str]:
    bash = os.environ.get("READYLINUX_BASH", "bash")
    return [bash, str(script), "--json"]


def run_preflight(script: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        preflight_argv(script),
        capture_output=True,
        text=True,
        check=False,
    )


def parse_report(result: subprocess.CompletedProcess) -> dict:
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit(f"record-yocto-preflight: preflight did not return JSON: {error}") from error
    if not isinstance(report, dict) or "verdict" not in report:
        raise SystemExit("record-yocto-preflight: preflight JSON is missing 'verdict'")
    return report


def inconsistent_ready_report(report: dict) -> str | None:
    """Return a reason when a "ready" verdict contradicts its own fields."""
    if report.get("verdict") != "ready":
        return None
    if report.get("missing_required"):
        return "verdict is ready but missing_required is not empty"
    required_tools = report.get("required")
    if isinstance(required_tools, dict) and any(not available for available in required_tools.values()):
        return "verdict is ready but a required host command is unavailable"
    builddir = report.get("builddir") or {}
    if not builddir.get("set"):
        return "verdict is ready but builddir is not set"
    return None


def repository_commit(repo: Path) -> str:
    git = os.environ.get("READYLINUX_GIT", "git")
    result = subprocess.run(
        [git, "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    commit = result.stdout.strip()
    if result.returncode != 0 or len(commit) != 40:
        raise SystemExit("record-yocto-preflight: cannot read the READY Linux commit via git rev-parse HEAD")
    return commit


def write_record(output: Path, record: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, output)


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)

    if args.check:
        path = Path(args.check)
        if not path.is_file():
            print(f"record-yocto-preflight: no such record: {path}", file=sys.stderr)
            return 8
        try:
            stored = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            print(f"record-yocto-preflight: {path} is not valid JSON: {error}", file=sys.stderr)
            return 8
        problems = validate_record(stored)
        if problems:
            for problem in problems:
                print(f"record-yocto-preflight: invalid record: {problem}", file=sys.stderr)
            return 8
        print(f"record-yocto-preflight: {path} is a valid preflight record")
        return 0

    if not args.output:
        print("record-yocto-preflight: OUTPUT path is required unless --check is used", file=sys.stderr)
        return 64

    script = Path(args.preflight_script) if args.preflight_script else Path(__file__).resolve().parent / "check-yocto-host.sh"
    repo = Path(args.repo) if args.repo else script.resolve().parent.parent

    if not script.is_file():
        raise SystemExit(f"record-yocto-preflight: preflight script not found: {script}")

    result = run_preflight(script)
    report = parse_report(result)
    verdict = report["verdict"]
    if verdict != "ready" or result.returncode != 0:
        print(
            f"record-yocto-preflight: preflight verdict is '{verdict}' (exit {result.returncode}); "
            "refusing to write a record that could be read as build evidence",
            file=sys.stderr,
        )
        return 3

    contradiction = inconsistent_ready_report(report)
    if contradiction is not None:
        print(
            f"record-yocto-preflight: refusing inconsistent report: {contradiction}",
            file=sys.stderr,
        )
        return 5

    record = {
        "schema_version": SCHEMA_VERSION,
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "readylinux_commit": repository_commit(repo),
        "scope": SCOPE,
        "preflight_command": " ".join(preflight_argv(script)),
        "preflight_exit_code": result.returncode,
        "preflight": report,
    }
    output = Path(args.output)
    if output.exists() and not args.force:
        print(
            f"record-yocto-preflight: {output} already exists; use --force to replace it",
            file=sys.stderr,
        )
        return 4
    write_record(output, record)
    print(f"record-yocto-preflight: wrote {args.output} (verdict ready)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
