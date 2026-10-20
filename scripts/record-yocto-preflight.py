#!/usr/bin/env python3
"""Record a read-only Yocto host preflight as auditable JSON evidence.

The recorder refuses to invent build results: it only captures the preflight
report plus provenance (UTC time, READY Linux commit) and states the scope.
Exit codes: 0 written, 3 preflight not ready, 4 output exists without --force.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
SCOPE = (
    "preflight-only: no BitBake metadata parse, no image build, no QEMU boot; "
    "this record is not build evidence"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record a read-only Yocto host preflight as JSON.")
    parser.add_argument("output", help="path of the JSON record to write")
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
