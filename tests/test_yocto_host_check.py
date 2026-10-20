import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-yocto-host.sh"


class YoctoHostCheckTests(unittest.TestCase):
    def test_script_shell_syntax(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_is_read_only_and_documents_bitbake_scope(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Installs/downloads nothing", text)
        self.assertIn("release-pinned Poky/OE-Core", text)
        self.assertNotRegex(text, r"(?m)^\s*(?:apt-get|apt|dnf|yum|zypper|curl|wget)\s+(?:install|download|fetch)")
        self.assertIn("if command -v bitbake >/dev/null 2>&1 && command -v bitbake-layers >/dev/null 2>&1", text)
        self.assertIn("BitBake executables found on PATH.", text)

    def test_reports_missing_host_tools_without_modifying_system(self):
        with tempfile.TemporaryDirectory() as temp:
            fakebin = Path(temp)
            for name in ("bash", "uname", "getconf"):
                source = Path("/usr/bin") / name
                if source.exists():
                    (fakebin / name).symlink_to(source)
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=ROOT,
                env={"PATH": str(fakebin), "ID": "debian"},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING gcc", result.stdout)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("no package changes made", result.stdout)

    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_reports_complete_when_required_commands_and_builddir_exist(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            builddir = root / "build"
            builddir.mkdir()
            for name in (
                "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
                "diffstat", "file", "gawk", "ip", "ping", "socat", "texi2any", "unzip",
                "wget", "xz", "zstd", "uname", "getconf",
            ):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT)],
                cwd=ROOT,
                env={"PATH": str(fakebin), "BUILDDIR": str(builddir)},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Preflight: required Debian host commands and BUILDDIR found", result.stdout)
        self.assertIn("BitBake must be supplied by a release-pinned Poky/OE-Core checkout", result.stdout)

    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_marks_missing_builddir_incomplete_when_tools_are_present(self):
        with tempfile.TemporaryDirectory() as temp:
            fakebin = Path(temp) / "bin"
            fakebin.mkdir()
            required = (
                "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
                "diffstat", "file", "gawk", "ip", "ping", "socat", "texi2any", "unzip",
                "wget", "xz", "zstd", "uname", "getconf",
            )
            for name in required:
                stub = fakebin / name
                stub.write_text("#!/bin/sh\\nexit 0\\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            env = {"PATH": str(fakebin)}
            env.pop("BUILDDIR", None)
            result = subprocess.run([bash_path, str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)
        self.assertNotIn("MISSING ", result.stdout)
        self.assertIn("BitBake must be supplied by a release-pinned Poky/OE-Core checkout", result.stdout)

    @unittest.skipIf(os.name == "nt", "Unix directory/file semantics required")
    def test_rejects_file_as_builddir(self):
        with tempfile.TemporaryDirectory() as temp:
            fakebin = Path(temp)
            file_builddir = fakebin / "not-a-directory"
            file_builddir.write_text("not a build directory", encoding="utf-8")
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT)],
                cwd=ROOT,
                env={"PATH": "/usr/bin:/bin", "BUILDDIR": str(file_builddir)},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)

    @unittest.skipIf(os.name == "nt", "Unix environment semantics required")
    def test_marks_absent_required_tool_even_with_valid_builddir_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            builddir = root / "build"
            builddir.mkdir()
            for name in ("bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio", "diffstat", "file", "gawk", "ip", "ping", "socat", "texi2any", "unzip", "wget", "xz", "zstd", "uname", "getconf"):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\\nexit 0\\n", encoding="utf-8")
                stub.chmod(0o755)
            (fakebin / "gcc").unlink()
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT)],
                cwd=ROOT,
                env={"PATH": str(fakebin), "BUILDDIR": str(builddir)},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING gcc", result.stdout)
        self.assertIn(f"BUILDDIR: {builddir}", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)

    def test_rejects_invalid_builddir_path(self):
        result = subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=ROOT,
            env={"PATH": "/usr/bin:/bin", "BUILDDIR": "/does/not/exist"},
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)


if __name__ == "__main__":
    unittest.main()
