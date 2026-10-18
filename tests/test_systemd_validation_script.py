import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-systemd-unit.sh"


class SystemdValidationScriptTests(unittest.TestCase):
    def test_helper_shell_syntax(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_helper_fails_closed_if_systemd_analyze_is_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            empty_bin = Path(temp) / "bin"
            empty_bin.mkdir()
            result = subprocess.run(
                ["bash", "-c", f"PATH='{empty_bin}'; export PATH; exec '/bin/bash' '{SCRIPT}'"],
                cwd=ROOT,
                env={"PATH": f"{empty_bin}:/usr/bin:/bin"},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("systemd-analyze is unavailable", result.stderr)
        self.assertNotIn("Verifying READY", result.stdout)

    def test_runtime_systemd_verify_when_available(self):
        probe = subprocess.run(["bash", "-lc", "command -v systemd-analyze"], capture_output=True, text=True)
        if probe.returncode:
            self.skipTest("systemd-analyze is unavailable on this host")
        result = subprocess.run(["bash", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Verifying READY systemd unit syntax", result.stdout)

    def test_script_documents_temporary_host_command_substitution(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("sed 's#^ExecStart=/usr/bin/readylinux .*#ExecStart=/bin/true#'", text)
        self.assertIn("mktemp -d", text)
        self.assertIn("systemd-analyze verify", text)


if __name__ == "__main__":
    unittest.main()
