import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "scripts/check-yocto-host.sh"
RECORDER = ROOT / "scripts/record-yocto-preflight.py"
SCHEMA = ROOT / "docs/YOCTO_PREFLIGHT_RECORD.schema.json"
EXAMPLE = ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json"
REQUIRED = (
    "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
    "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping",
    "socat", "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd",
)
OPTIONAL = ("bitbake", "bitbake-layers", "qemu-system-x86_64", "sha256sum")


def parse_jsonschema_subset(value, schema, path="$", errors=None):
    """Small dependency-free JSON Schema validator for this checked-in schema."""
    errors = [] if errors is None else errors
    expected = schema.get("type")
    type_ok = True
    if expected == "object":
        type_ok = isinstance(value, dict)
    elif expected == "array":
        type_ok = isinstance(value, list)
    elif expected == "string":
        type_ok = isinstance(value, str)
    elif expected == "integer":
        type_ok = isinstance(value, int) and not isinstance(value, bool)
    elif expected == "boolean":
        type_ok = isinstance(value, bool)
    elif isinstance(expected, list):
        type_ok = any(parse_jsonschema_subset(value, {"type": item}, path) == [] for item in expected)
    if not type_ok:
        errors.append(f"{path}: expected {expected}")
        return errors

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string shorter than minLength")
        if "pattern" in schema:
            pattern = schema["pattern"].replace("\\\\", "\\")
            if not __import__("re").search(pattern, value):
                errors.append(f"{path}: string does not match pattern")
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value):
        errors.append(f"{path}: below minimum")
    if isinstance(value, list):
        if schema.get("uniqueItems") and len(value) != len(set(value)):
            errors.append(f"{path}: duplicate array items")
        for i, item in enumerate(value):
            parse_jsonschema_subset(item, schema.get("items", {}), f"{path}[{i}]", errors)
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing key {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(schema.get("properties", {}))
            if extra:
                errors.append(f"{path}: unexpected keys {sorted(extra)}")
        properties = schema.get("properties", {})
        extra_schema = schema.get("additionalProperties")
        for key, item in value.items():
            if key in properties:
                parse_jsonschema_subset(item, properties[key], f"{path}.{key}", errors)
            elif isinstance(extra_schema, dict):
                parse_jsonschema_subset(item, extra_schema, f"{path}.{key}", errors)
    return errors


def linux_path(path):
    if os.name != "nt":
        return str(path)
    result = subprocess.run(
        ["bash", "-lc", "cygpath -u \"$1\"", "bash", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return str(path)


def write_stub(path, content):
    path.write_text("#!/bin/sh\n" + content + "\n", encoding="utf-8")
    path.chmod(0o755)


def fake_linux_env(root, fakebin, *, builddir=None, os_release=None, include_dpkg=True):
    os_release = os_release or (root / "os-release")
    os_release.write_text(
        'PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\nVERSION_ID="13"\n',
        encoding="utf-8",
    )
    if include_dpkg:
        write_stub(fakebin / "dpkg-query", "printf '1.2.3\\n'")
    env = os.environ.copy()
    env.update({
        "PATH": f"{linux_path(fakebin)}:{os.environ.get('PATH', '')}",
        "READYLINUX_OS_RELEASE": linux_path(os_release),
    })
    if builddir is not None:
        env["BUILDDIR"] = linux_path(builddir)
    else:
        env.pop("BUILDDIR", None)
    return env


class HostPreflightJsonTests(unittest.TestCase):
    def make_stub_host(self, root, *, missing=(), include_dpkg=True, include_optional=True):
        fakebin = root / "bin"
        fakebin.mkdir()
        for name in REQUIRED:
            if name not in missing:
                write_stub(fakebin / name, "exit 0")
        if include_optional:
            for name in OPTIONAL:
                write_stub(fakebin / name, "exit 0")
        builddir = root / "build"
        builddir.mkdir()
        env = fake_linux_env(root, fakebin, builddir=builddir, include_dpkg=include_dpkg)
        env["PATH"] = f"{linux_path(fakebin)}:/usr/bin:/bin"
        env["READYLINUX_OS_RELEASE"] = linux_path(root / "os-release")
        return fakebin, builddir, env

    def test_ready_report_has_both_text_and_evidence_schema_provenance(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, env = self.make_stub_host(root)
            env["PATH"] = f"{linux_path(fakebin)}:{os.environ.get('PATH', '')}"
            env["READYLINUX_OS_RELEASE"] = linux_path(root / "os-release")
            bash_path = "bash" if os.name == "nt" else subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run([bash_path, linux_path(PREFLIGHT), "--json"], env=env, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "ready")
        self.assertEqual(report["os"]["version_id"], "13")
        self.assertEqual(report["packages"]["gcc"], "1.2.3")
        self.assertEqual(report["packages"]["qemu-system-x86"], "1.2.3")
        errors = parse_jsonschema_subset(report, schema["properties"]["preflight"])
        self.assertEqual(errors, [])
        record = {
            "schema_version": 1,
            "recorded_utc": "2026-10-20T20:00:00Z",
            "readylinux_commit": "a" * 40,
            "scope": "preflight-only; not build evidence",
            "preflight_command": "bash check-yocto-host.sh --json",
            "preflight_exit_code": 0,
            "preflight": report,
        }
        record_schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(parse_jsonschema_subset(record, record_schema), [])

    def test_incomplete_report_lists_exact_missing_required_commands(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, env = self.make_stub_host(root, missing={"gcc", "lz4c"})
            env["PATH"] = linux_path(fakebin)
            bash_path = "bash" if os.name == "nt" else subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run([bash_path, linux_path(PREFLIGHT), "--json"], env=env, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "incomplete")
        self.assertEqual(report["missing_required"], ["gcc", "lz4c"])
        errors = parse_jsonschema_subset(report, json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]["preflight"])
        self.assertEqual(errors, [])

    def test_non_linux_report_has_no_fake_command_or_package_claims(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            env = fake_linux_env(root, fakebin, include_dpkg=False)
            env["READYLINUX_OS_RELEASE"] = linux_path(root / "missing-os-release")
            bash_path = "bash" if os.name == "nt" else subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run([bash_path, linux_path(PREFLIGHT), "--json"], env=env, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "not-a-linux-host")
        self.assertEqual(report["required"], {})
        self.assertEqual(report["missing_required"], [])
        self.assertEqual(report["packages"], {})
        self.assertEqual(report["os"]["version_id"], None)

    def test_package_versions_are_null_without_dpkg_query(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, env = self.make_stub_host(root, include_dpkg=False)
            env["PATH"] = linux_path(fakebin)
            bash_path = "bash" if os.name == "nt" else subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run([bash_path, linux_path(PREFLIGHT), "--json"], env=env, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "ready")
        self.assertEqual(report["builddir"]["set"], True)
        self.assertIsNone(report["packages"]["gcc"])

    @unittest.skipIf(os.name == "nt", "recorder integration requires WSL/Linux executable semantics")
    def test_preflight_recorder_writes_and_check_validates_host_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, env = self.make_stub_host(root)
            env["READYLINUX_BASH"] = "/usr/bin/bash"
            env["READYLINUX_GIT"] = shutil.which("git") or "git"
            output = root / "record.json"
            result = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT)],
                env=env,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads(output.read_text(encoding="utf-8"))
            schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            errors = parse_jsonschema_subset(record, schema)
            self.assertEqual(errors, [])
            checked = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)


if __name__ == "__main__":
    unittest.main()
