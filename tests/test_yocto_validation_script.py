import subprocess
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

    def test_script_checks_build_confs_and_layer_registration(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for check in ("BUILDDIR", "conf/bblayers.conf", "conf/local.conf", "bitbake", "bblayers.conf", "bitbake -p"):
            self.assertIn(check, text)
        self.assertNotRegex(text, r"(?m)^\s*(?:git clone|curl|wget)\b")


if __name__ == "__main__":
    unittest.main()
