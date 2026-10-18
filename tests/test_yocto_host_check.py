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


if __name__ == "__main__":
    unittest.main()
