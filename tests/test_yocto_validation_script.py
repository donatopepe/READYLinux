import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-yocto-env.sh"


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

    def run_with_builddir(self, builddir, *, with_bitbake=True):
        temp_path = tempfile.TemporaryDirectory()
        bindir = Path(temp_path.name) / "bin"
        bindir.mkdir()
        if with_bitbake:
            fake = bindir / "bitbake"
            fake.write_text("#!/bin/sh\nprintf 'FAKE_BITBAKE %s\\n' \"$*\"\n", encoding="utf-8")
            fake.chmod(0o755)
        env = {"PATH": f"{bindir}:/usr/bin:/bin", "BUILDDIR": str(builddir)}
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
            layer_path = "/d/repos/ReadyLinux/meta-readylinux"
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_checks_build_confs_and_layer_registration(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for check in ("BUILDDIR", "conf/bblayers.conf", "conf/local.conf", "bitbake", "bblayers.conf", "bitbake -p"):
            self.assertIn(check, text)
        self.assertNotRegex(text, r"(?m)^\s*(?:git clone|curl|wget)\b")


if __name__ == "__main__":
    unittest.main()
