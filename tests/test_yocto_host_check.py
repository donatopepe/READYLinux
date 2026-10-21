import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-yocto-host.sh"
DEBIAN_OS_RELEASE = (
    'PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\nID_LIKE=debian\nVERSION_ID="13"\n'
)


def debian_os_release(directory):
    path = Path(directory) / "os-release"
    path.write_text(DEBIAN_OS_RELEASE, encoding="utf-8")
    return str(path)


def host_env(directory, **extra):
    env = {"READYLINUX_OS_RELEASE": debian_os_release(directory)}
    env.update(extra)
    return env


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
        self.assertIn("Environment tools (not provided by this probe):", text)
        self.assertIn("optional_commands=(bitbake bitbake-layers", text)
        self.assertIn("package_versions_json()", text)
        self.assertIn("version_id", text)
        self.assertIn("packages", text)
        self.assertIn("Environment tools (not provided by this probe):", text)
        self.assertIn("Preflight: required Debian host commands and BUILDDIR found", text)
        self.assertIn("Preflight: INCOMPLETE (read-only; no package changes made).", text)

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
                env=host_env(temp, PATH=str(fakebin), ID="debian"),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING gcc", result.stdout)
        self.assertIn("BitBake must be supplied by a release-pinned Poky/OE-Core checkout.", result.stdout)
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
                "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping", "socat",
                "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd", "uname", "getconf", "bitbake", "bitbake-layers",
            ):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT)],
                cwd=ROOT,
                env=host_env(root, PATH=str(fakebin), BUILDDIR=str(builddir)),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Preflight: required Debian host commands and BUILDDIR found", result.stdout)
        self.assertIn("BitBake executables found on PATH.", result.stdout)
        self.assertNotIn("BitBake must be supplied by a release-pinned Poky/OE-Core checkout", result.stdout)
        self.assertIn("Environment tools (not provided by this probe):", result.stdout)
        self.assertIn("FOUND   bitbake", result.stdout)
        self.assertIn("FOUND   bitbake-layers", result.stdout)

    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_marks_missing_builddir_incomplete_when_tools_are_present(self):
        with tempfile.TemporaryDirectory() as temp:
            fakebin = Path(temp) / "bin"
            fakebin.mkdir()
            required = (
                "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
                "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping", "socat",
                "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd", "uname", "getconf",
            )
            required = tuple(required) + ("bitbake", "bitbake-layers")
            for name in required:
                stub = fakebin / name
                stub.write_text("#!/bin/sh\\nexit 0\\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            env = host_env(temp, PATH=str(fakebin))
            env.pop("BUILDDIR", None)
            result = subprocess.run([bash_path, str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)
        self.assertNotIn("MISSING ", result.stdout)
        self.assertIn("BitBake executables found on PATH.", result.stdout)
        self.assertNotIn("BitBake must be supplied by a release-pinned Poky/OE-Core checkout", result.stdout)
        self.assertIn("ABSENT  qemu-system-x86_64", result.stdout)
        self.assertIn("ABSENT  sha256sum", result.stdout)

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
                env=host_env(temp, PATH="/usr/bin:/bin", BUILDDIR=str(file_builddir)),
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
                env=host_env(root, PATH=str(fakebin), BUILDDIR=str(builddir)),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING gcc", result.stdout)
        self.assertIn(f"BUILDDIR: {builddir}", result.stdout)
        self.assertIn("ABSENT  bitbake", result.stdout)
        self.assertIn("ABSENT  bitbake-layers", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)

    def test_rejects_invalid_builddir_path(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=ROOT,
                env=host_env(temp, PATH="/usr/bin:/bin", BUILDDIR="/does/not/exist"),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("BUILDDIR: unset", result.stdout)
        self.assertIn("Preflight: INCOMPLETE", result.stdout)

    def test_fails_closed_when_no_linux_os_release_is_available(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=ROOT,
                env={"READYLINUX_OS_RELEASE": str(Path(temp) / "missing-os-release")},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("OS: /etc/os-release unavailable", result.stdout)
        self.assertIn("WRONG-ENVIRONMENT", result.stdout)
        self.assertIn("Preflight: NOT-A-LINUX-HOST", result.stdout)
        self.assertNotIn("Preflight: INCOMPLETE", result.stdout)


    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_json_report_is_machine_readable_and_ready_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            builddir = root / "build"
            builddir.mkdir()
            for name in (
                "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
                "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping", "socat",
                "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd", "uname", "getconf", "bitbake", "bitbake-layers",
            ):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT), "--json"],
                cwd=ROOT,
                env=host_env(root, PATH=str(fakebin), BUILDDIR=str(builddir)),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["verdict"], "ready")
        self.assertEqual(report["os"]["version_id"], "13")
        self.assertIn("gcc", report["packages"])
        self.assertIn("qemu-system-x86", report["packages"])
        self.assertEqual(report["missing_required"], [])
        self.assertTrue(report["required"]["gcc"])
        self.assertTrue(report["optional"]["bitbake"])
        self.assertEqual(report["builddir"], {"set": True, "path": str(builddir)})
        self.assertIsInstance(report["cpus"], int)
        self.assertTrue(report["arch"])

    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_json_report_lists_missing_required_tools_and_incomplete_verdict(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            for name in ("bash", "git", "g++", "make", "python3", "uname", "getconf"):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT), "--json"],
                cwd=ROOT,
                env=host_env(root, PATH=str(fakebin)),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "incomplete")
        self.assertEqual(report["os"]["version_id"], "13")
        self.assertIn("gcc", report["packages"])
        self.assertFalse(report["required"]["gcc"])
        self.assertIn("gcc", report["missing_required"])
        self.assertNotIn("git", report["missing_required"])
        self.assertEqual(report["builddir"], {"set": False, "path": None})

    @unittest.skipIf(os.name == "nt", "PATH command stubs require Unix")
    def test_json_package_versions_are_null_when_dpkg_query_is_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            builddir = root / "build"
            builddir.mkdir()
            commands = (
                "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
                "diffstat", "file", "gawk", "ip", "lz4c", "patch", "perl", "ping",
                "socat", "tar", "texi2any", "unzip", "wget", "xargs", "xz", "zstd",
                "uname", "getconf", "bitbake", "bitbake-layers",
            )
            for name in commands:
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            bash_path = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            result = subprocess.run(
                [bash_path, str(SCRIPT), "--json"],
                cwd=ROOT,
                env=host_env(root, PATH=f"{fakebin}:/usr/bin:/bin", BUILDDIR=str(builddir)),
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "ready")
        self.assertTrue(report["packages"])
        self.assertTrue(all(isinstance(v, str) or v is None for v in report["packages"].values()))

    def test_json_report_marks_wrong_environment_without_fake_command_claims(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                ["bash", str(SCRIPT), "--json"],
                cwd=ROOT,
                env={"READYLINUX_OS_RELEASE": str(Path(temp) / "missing-os-release")},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "not-a-linux-host")
        self.assertEqual(report["required"], {})
        self.assertEqual(report["packages"], {})
        self.assertEqual(report["os"]["version_id"], None)
        self.assertEqual(report["missing_required"], [])
        self.assertEqual(report["builddir"], {"set": False, "path": None})

    def test_rejects_unknown_argument_with_usage_exit_code(self):
        result = subprocess.run(["bash", str(SCRIPT), "--verbose"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 64)
        self.assertIn("Usage:", result.stderr)

if __name__ == "__main__":
    unittest.main()
