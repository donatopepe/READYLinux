import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-yocto-env.sh"


def shell_pwd(path):
    result = subprocess.run(["bash", "-lc", "cd \"$1\" && pwd -P", "bash", str(path)], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def to_shell_path(path):
    if os.name == "nt":
        result = subprocess.run(["bash", "-lc", "cygpath -u \"$1\"", "bash", str(path)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return str(path)




class YoctoValidationScriptTests(unittest.TestCase):
    def test_script_is_shell_syntax_valid(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_fails_closed_without_bitbake_environment(self):
        result = subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=ROOT,
            env={"PATH": "/usr/bin:/bin"},
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("source the target build environment first", result.stderr)
        self.assertNotIn("bitbake -p", result.stdout)

    def run_with_builddir(self, builddir, *, with_bitbake=True, bitbake_exit=0):
        temp_path = tempfile.TemporaryDirectory()
        bindir = Path(temp_path.name) / "bin"
        bindir.mkdir()
        if with_bitbake:
            fake = bindir / "bitbake"
            fake.write_text(f"#!/bin/sh\nprintf 'FAKE_BITBAKE %s %s\\n' \"$*\" \"$PWD\"\nexit {bitbake_exit}\n", encoding="utf-8")
            fake.chmod(0o755)
        env = {"PATH": f"{bindir}:/usr/bin:/bin", "BUILDDIR": to_shell_path(builddir)}
        return subprocess.run(["bash", str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True), temp_path

    def test_script_fails_when_bitbake_is_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            (builddir / "conf").mkdir()
            (builddir / "conf/bblayers.conf").write_text("", encoding="utf-8")
            (builddir / "conf/local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, with_bitbake=False)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("bitbake is not available", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    def test_script_fails_when_build_configs_are_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            result, fake_root = self.run_with_builddir(Path(temp))
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "temp directories on Windows are outside the WSL filesystem")
    def test_script_accepts_build_directory_with_spaces(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp) / "build tree with spaces"
            conf = builddir / "conf"
            conf.mkdir(parents=True)
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            expected_path = shell_pwd(builddir)
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Build directory: {expected_path}", result.stdout)
        self.assertIn(f"FAKE_BITBAKE -p {expected_path}", result.stdout)

    def test_script_accepts_symlinked_build_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actual = root / "build actual"
            conf = actual / "conf"
            conf.mkdir(parents=True)
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            alias = root / "build-link"
            alias.symlink_to(actual, target_is_directory=True)
            result, fake_root = self.run_with_builddir(alias)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_fails_when_layer_is_not_registered(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            (conf / "bblayers.conf").write_text("BBLAYERS = \\\"/some/other/layer\\\"\\n", encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("add", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    def test_script_runs_metadata_parse_only_after_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        announced_builddir = next(line.removeprefix("Build directory: ") for line in result.stdout.splitlines() if line.startswith("Build directory: "))
        self.assertTrue(announced_builddir)
        self.assertIn(f"FAKE_BITBAKE -p {announced_builddir}", result.stdout)

    def test_script_propagates_bitbake_parse_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, bitbake_exit=37)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 37)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_checks_build_confs_and_layer_registration(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for check in ("BUILDDIR", "conf/bblayers.conf", "conf/local.conf", "bitbake", "bblayers.conf", "bitbake -p"):
            self.assertIn(check, text)
        self.assertNotRegex(text, r"(?m)^\s*(?:git clone|curl|wget)\b")


if __name__ == "__main__":
    unittest.main()
