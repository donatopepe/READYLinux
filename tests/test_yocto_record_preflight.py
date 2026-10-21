import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDER = ROOT / "scripts/record-yocto-preflight.py"
EXAMPLE = ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json"
PREFLIGHT = ROOT / "scripts/check-yocto-host.sh"
REAL_BASH = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
REAL_GIT = subprocess.check_output(["bash", "-lc", "command -v git"], text=True).strip()
REQUIRED = (
    "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
    "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping", "socat",
    "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd", "uname", "getconf",
)


def make_ready_host(root):
    fakebin = root / "bin"
    fakebin.mkdir()
    for name in REQUIRED + ("bitbake", "bitbake-layers"):
        stub = fakebin / name
        stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        stub.chmod(0o755)
    builddir = root / "build"
    builddir.mkdir()
    os_release = root / "os-release"
    os_release.write_text('PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\nID_LIKE=debian\n', encoding="utf-8")
    return fakebin, builddir, os_release


@unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
class ReadyRecorderTests(unittest.TestCase):
    def test_writes_record_with_provenance_and_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, os_release = make_ready_host(root)
            output = root / "evidence" / "preflight.json"
            result = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT)],
                cwd=ROOT,
                env={
                    "READYLINUX_BASH": REAL_BASH, "READYLINUX_GIT": REAL_GIT,
                    "PATH": str(fakebin),
                    "BUILDDIR": str(builddir),
                    "READYLINUX_OS_RELEASE": str(os_release),
                },
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], 1)
        self.assertRegex(record["readylinux_commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(record["recorded_utc"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertIn("not build evidence", record["scope"])
        self.assertIn("--json", record["preflight_command"])
        self.assertEqual(record["preflight_exit_code"], 0)
        self.assertEqual(record["preflight"]["verdict"], "ready")
        self.assertEqual(record["preflight"]["missing_required"], [])
        self.assertTrue(record["preflight"]["optional"]["bitbake"])
        self.assertEqual(record["preflight"]["required"]["gcc"], True)

    def test_refuses_to_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin, builddir, os_release = make_ready_host(root)
            output = root / "preflight.json"
            output.write_text('{"existing": true}\n', encoding="utf-8")
            env = {
                "READYLINUX_BASH": REAL_BASH, "READYLINUX_GIT": REAL_GIT,
                "PATH": str(fakebin),
                "BUILDDIR": str(builddir),
                "READYLINUX_OS_RELEASE": str(os_release),
            }
            blocked = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 4, blocked.stdout + blocked.stderr)
            self.assertIn("--force", blocked.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), {"existing": True})
            forced = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT), "--force"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)


class UnsafeRecorderTests(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "needs a Linux host to be merely incomplete")
    def test_refuses_incomplete_host_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "preflight.json"
            fakebin = root / "bin"
            fakebin.mkdir()
            for name in ("bash", "git", "uname", "getconf"):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            os_release = root / "os-release"
            os_release.write_text('PRETTY_NAME="Debian GNU/Linux 13 (trixie)"ID=debian', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT), "--preflight-script", str(PREFLIGHT)],
                cwd=ROOT,
                env={"READYLINUX_BASH": REAL_BASH, "READYLINUX_GIT": REAL_GIT, "PATH": str(fakebin), "READYLINUX_OS_RELEASE": str(os_release)},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertIn("refusing to write", result.stderr)
            self.assertIn("incomplete", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_report_where_required_map_hides_missing_command(self):
        report = json.dumps({
            "schema_version": 1,
            "os": {"name": "Debian", "id": "debian"},
            "arch": "x86_64",
            "cpus": 2,
            "required": {"gcc": False},
            "missing_required": [],
            "optional": {},
            "builddir": {"set": True, "path": "/build"},
            "verdict": "ready",
        })
        with tempfile.TemporaryDirectory() as temp:
            result, output = self._run_fake_preflight(Path(temp), report)
            self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
            self.assertIn("required host command is unavailable", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_report_with_spurious_missing_command_name(self):
        report = json.dumps({
            "schema_version": 1,
            "os": {"name": "Debian", "id": "debian"},
            "arch": "x86_64",
            "cpus": 2,
            "required": {"gcc": True},
            "missing_required": ["gcc"],
            "optional": {},
            "builddir": {"set": True, "path": "/build"},
            "verdict": "ready",
        })
        with tempfile.TemporaryDirectory() as temp:
            result, output = self._run_fake_preflight(Path(temp), report)
            self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
            self.assertIn("missing_required is not empty", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_non_linux_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "preflight.json"
            env = dict(os.environ)
            env["READYLINUX_OS_RELEASE"] = str(root / "missing-os-release")
            result = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertIn("not-a-linux-host", result.stderr)
            self.assertFalse(output.exists())


    def _run_fake_preflight(self, root, report_json):
        fake_preflight = root / "fake-preflight.sh"
        lines = [
            "#!/bin/sh",
            "cat <<'JSON'",
            report_json,
            "JSON",
            "exit 0",
            "",
        ]
        fake_preflight.write_text(chr(10).join(lines), encoding="utf-8")
        fake_preflight.chmod(0o755)
        output = root / "record.json"
        result = subprocess.run(
            [
                sys.executable,
                str(RECORDER),
                str(output),
                "--repo",
                str(ROOT),
                "--preflight-script",
                str(fake_preflight),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return result, output

    def test_refuses_report_that_claims_ready_without_builddir(self):
        report = json.dumps(
            {
                "schema_version": 1,
                "os": {"name": "x", "id": "debian"},
                "arch": "x86_64",
                "cpus": 1,
                "required": {},
                "missing_required": [],
                "optional": {},
                "builddir": {"set": False, "path": None},
                "verdict": "ready",
            }
        )
        with tempfile.TemporaryDirectory() as temp:
            result, output = self._run_fake_preflight(Path(temp), report)
            self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
            self.assertIn("builddir is not set", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_report_that_claims_ready_with_missing_commands(self):
        report = json.dumps(
            {
                "schema_version": 1,
                "os": {"name": "x", "id": "debian"},
                "arch": "x86_64",
                "cpus": 1,
                "required": {"gcc": False},
                "missing_required": ["gcc"],
                "optional": {},
                "builddir": {"set": True, "path": "/build"},
                "verdict": "ready",
            }
        )
        with tempfile.TemporaryDirectory() as temp:
            result, output = self._run_fake_preflight(Path(temp), report)
            self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
            self.assertIn("missing_required is not empty", result.stderr)
            self.assertFalse(output.exists())

    def test_check_accepts_the_documented_example(self):
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(set(example), {"schema_version", "recorded_utc", "readylinux_commit", "scope", "preflight_command", "preflight_exit_code", "preflight"})
        self.assertEqual(set(example["preflight"]), {"schema_version", "os", "arch", "cpus", "required", "missing_required", "optional", "builddir", "verdict"})
        self.assertRegex(example["readylinux_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(example["preflight_exit_code"], 0)
        self.assertEqual(example["preflight"]["verdict"], "ready")
        self.assertTrue(example["preflight"]["builddir"]["set"])
        self.assertTrue(example["preflight"]["optional"]["bitbake"])
        self.assertTrue(example["preflight"]["optional"]["bitbake-layers"])
        result = subprocess.run(
            [sys.executable, str(RECORDER), "--check", str(EXAMPLE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("is a valid preflight record", result.stdout)

    def test_check_rejects_non_ready_verdict_record(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight"]["verdict"] = "incomplete"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("verdict must be ready", result.stderr)

    def test_check_rejects_string_preflight_exit_code(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight_exit_code"] = "0"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("preflight_exit_code must be integer 0", result.stderr)

    def test_check_rejects_empty_architecture(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight"]["arch"] = "  "
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("preflight.arch must be a non-empty string", result.stderr)

    def test_check_rejects_non_string_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["scope"] = {"claim": "not build evidence"}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("scope must state that the record is not build evidence", result.stderr)

    def test_check_rejects_future_timestamp(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["recorded_utc"] = "2999-12-31T23:59:59Z"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("recorded_utc is in the future", result.stderr)

    def test_check_rejects_impossible_calendar_timestamp(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["recorded_utc"] = "2026-02-30T12:00:00Z"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("not a valid calendar timestamp", result.stderr)

    def test_check_rejects_a_record_that_claims_ready_without_builddir(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads((ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json").read_text(encoding="utf-8"))
            record["preflight"]["builddir"] = {"set": False, "path": None}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("builddir is not set", result.stderr)

    def test_check_rejects_missing_and_unexpected_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads((ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json").read_text(encoding="utf-8"))
            record.pop("preflight_command")
            record["unexpected"] = True
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("missing top-level key: preflight_command", result.stderr)
        self.assertIn("unexpected top-level keys: unexpected", result.stderr)

    def test_check_rejects_scope_that_hides_the_evidence_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads((ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json").read_text(encoding="utf-8"))
            record["scope"] = "full build and boot verified"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("not build evidence", result.stderr)

    def test_check_rejects_boolean_cpu_count(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight"]["cpus"] = True
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("must be a non-negative integer, not a boolean", result.stderr)

    def test_check_rejects_empty_os_identity_and_invalid_command_maps(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight"]["os"]["id"] = ""
            record["preflight"]["required"] = {"": True, "gcc": 1}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("os name and id must be non-empty", result.stderr)
        self.assertIn("required must map non-empty command names to booleans", result.stderr)

    def test_check_requires_builddir_path_to_match_its_set_flag(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            record["preflight"]["builddir"] = {"set": False, "path": "/contradiction"}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(record_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 8, result.stdout + result.stderr)
        self.assertIn("path must be null when set is false", result.stderr)

    def test_check_rejects_invalid_json_and_missing_files(self):
        with tempfile.TemporaryDirectory() as temp:
            broken = Path(temp) / "broken.json"
            broken.write_text("{not json", encoding="utf-8")
            bad_json = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(broken)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            missing = subprocess.run(
                [sys.executable, str(RECORDER), "--check", str(Path(temp) / "absent.json")],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(bad_json.returncode, 8, bad_json.stdout + bad_json.stderr)
        self.assertIn("not valid JSON", bad_json.stderr)
        self.assertEqual(missing.returncode, 8, missing.stdout + missing.stderr)
        self.assertIn("no such record", missing.stderr)

if __name__ == "__main__":
    unittest.main()
