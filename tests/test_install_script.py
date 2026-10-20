import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"
SETUP_AI = ROOT / "setup-ai-cpu.sh"
BASH = "bash" if os.name == "nt" else (subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip() or "bash")


class InstallScriptTests(unittest.TestCase):
    def test_install_is_user_scoped_and_never_uses_sudo_or_network(self):
        text = INSTALL.read_text(encoding="utf-8")
        self.assertIn("set -euo pipefail", text)
        self.assertNotRegex(text, r"(?m)^\s*sudo\b")
        self.assertNotRegex(text, r"(?m)^\s*(?:apt|apt-get|dnf|yum|zypper|curl|wget)\b")
        self.assertNotRegex(text, r'(?m)(?:install -m \d+ --?|>)\s*"?(?:/usr|/etc|/opt)/')
        self.assertIn('${XDG_DATA_HOME:-$HOME/.local/share}', text)
        self.assertIn('$HOME/.local/bin', text)

    def test_install_copies_application_and_wrapper_into_a_temporary_home(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "home"
            data = Path(temp) / "data"
            home.mkdir()
            result = subprocess.run(
                [BASH, str(INSTALL)],
                cwd=ROOT,
                env={"HOME": str(home), "XDG_DATA_HOME": str(data), "PATH": os.environ.get("PATH", "/usr/bin:/bin")},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            app_dir = data / "readylinux/app"
            wrapper = home / ".local/bin/readylinux"
            for name in ("readylinux.py", "ai_local.py", "vibe.py"):
                self.assertTrue((app_dir / name).is_file(), name)
            self.assertTrue(wrapper.is_file())
            self.assertTrue(os.access(wrapper, os.X_OK) or os.name == "nt")
            wrapper_text = wrapper.read_text(encoding="utf-8")
            self.assertIn(str(app_dir / "readylinux.py").replace("\\", "/"), wrapper_text.replace("\\", "/"))
            self.assertTrue(wrapper_text.startswith("#!/usr/bin/env bash"))
            self.assertEqual(sorted(path.name for path in home.rglob("*") if path.is_file()), ["readylinux"])
            for forbidden in ("/etc", "/usr", "/opt"):
                self.assertFalse(any(forbidden in str(path) for path in home.rglob("*")), forbidden)

    def test_install_fails_closed_without_python3(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "home"
            home.mkdir()
            empty_path = Path(temp) / "empty"
            empty_path.mkdir()
            result = subprocess.run(
                [BASH, str(INSTALL)],
                cwd=ROOT,
                env={"HOME": str(home), "XDG_DATA_HOME": str(home), "PATH": str(empty_path)},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("python3", result.stderr)
            self.assertFalse((home / ".local/bin/readylinux").exists())


class SetupAiScriptTests(unittest.TestCase):
    def test_setup_ai_is_opt_in_pinned_and_never_escalates(self):
        text = SETUP_AI.read_text(encoding="utf-8")
        self.assertIn("set -euo pipefail", text)
        self.assertNotRegex(text, r"(?m)^\s*sudo\b")
        self.assertNotIn("systemctl", text)
        self.assertIn("MODEL_SHA='cc324af070c2ecbfd324a30884d2f951a7ff756aba85cb811a6ec436933bb046'", text)
        self.assertIn("sha256sum", text)
        self.assertIn("| sha256sum -c -", text)
        self.assertIn("CPU-only", text)
        self.assertIn("Non installa servizi di sistema, non usa sudo e non abilita alcuna API cloud.", text)

    def test_setup_ai_fails_closed_when_a_required_tool_is_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "home"
            home.mkdir()
            empty_path = Path(temp) / "empty"
            empty_path.mkdir()
            result = subprocess.run(
                [BASH, str(SETUP_AI)],
                cwd=ROOT,
                env={"HOME": str(home), "XDG_DATA_HOME": str(home), "PATH": str(empty_path)},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Manca:", result.stderr)
            self.assertEqual([path for path in home.rglob("*")], [])


if __name__ == "__main__":
    unittest.main()
