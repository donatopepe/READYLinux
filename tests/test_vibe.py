import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vibe import VibeError, VibeWorkspace
from readylinux import ReadyLinux


class VibeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ai = Mock()
        self.v = VibeWorkspace(self.root / "projects", self.ai)
        self.v.select("hello", create=True)

    def tearDown(self):
        self.tmp.cleanup()

    def stage(self, files, summary="test"):
        return self.v.stage_json(json.dumps({"summary": summary, "files": files}))

    def test_create_diff_approval_and_undo(self):
        diff = self.stage([{"path": "src/main.py", "content": 'print("Ciao")\n'}])
        self.assertIn("NON APPLICATA", diff)
        path = self.root / "projects/hello/src/main.py"
        self.assertFalse(path.exists())
        self.assertIn("applicata", self.v.apply())
        self.assertEqual(path.read_text(), 'print("Ciao")\n')
        self.assertIn("0 errori", self.v.check())
        self.assertIn("ripristinata", self.v.undo())
        self.assertFalse(path.exists())

    def test_edit_project_then_undo_restores_previous_content(self):
        file = self.root / "projects/hello/main.py"
        file.write_text('print("A")\n')
        self.stage([{"path": "main.py", "content": 'print("B")\n'}])
        self.assertIn("-print", self.v.diff())
        self.v.apply()
        self.assertEqual(file.read_text(), 'print("B")\n')
        self.v.undo()
        self.assertEqual(file.read_text(), 'print("A")\n')

    def test_modification_after_proposal_blocks_apply(self):
        file = self.root / "projects/hello/main.py"
        file.write_text("x = 1\n")
        self.stage([{"path": "main.py", "content": "x = 2\n"}])
        file.write_text("manual edit\n")
        with self.assertRaises(VibeError):
            self.v.apply()
        self.assertEqual(file.read_text(), "manual edit\n")

    def test_modification_after_apply_blocks_undo(self):
        self.stage([{"path": "main.py", "content": "x = 1\n"}])
        self.v.apply()
        file = self.root / "projects/hello/main.py"
        file.write_text("user change\n")
        with self.assertRaises(VibeError):
            self.v.undo()
        self.assertEqual(file.read_text(), "user change\n")

    def test_path_traversal_and_hidden_files_rejected(self):
        for path in ("../outside.py", "/tmp/evil.py", "a/../../x.py", ".env", "dir/.private.py", "main.sh", "C:\\evil.py"):
            with self.subTest(path=path), self.assertRaises(VibeError):
                self.stage([{"path": path, "content": "unsafe"}])
        self.assertFalse((self.root / "outside.py").exists())

    def test_symlink_escape_rejected(self):
        outside = self.root / "elsewhere"
        outside.mkdir()
        (self.root / "projects/hello/link").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(VibeError):
            self.stage([{"path": "link/evil.py", "content": "yes"}])
        self.assertFalse((outside / "evil.py").exists())

    def test_duplicate_and_big_files_rejected(self):
        with self.assertRaises(VibeError):
            self.stage([{"path": "x.py", "content": "a"}, {"path": "x.py", "content": "b"}])
        with self.assertRaises(VibeError):
            self.stage([{"path": "x.py", "content": "a" * 14001}])
        with self.assertRaises(VibeError):
            self.v.stage_json("not json")

    def test_generation_model_output_only_proposal(self):
        self.ai.propose_project.return_value = json.dumps({"summary": "A", "files": [{"path": "main.py", "content": "print(1)"}]})
        text = self.v.propose("crea un programma")
        self.assertIn("NON APPLICATA", text)
        self.assertFalse((self.root / "projects/hello/main.py").exists())
        self.assertIn("crea un programma", self.ai.propose_project.call_args.args)
        self.assertIn("main.py", self.v.diff())

    def test_check_syntax_never_executes_generated_code(self):
        marker = self.root / "executed.txt"
        source = f"open({str(marker)!r},'w').write('bad')\n"
        self.stage([{"path": "main.py", "content": source}])
        self.v.apply()
        self.assertIn("0 errori", self.v.check())
        self.assertFalse(marker.exists())

    def test_explicit_run_only(self):
        self.stage([{"path": "main.py", "content": 'print("Works")\n'}])
        self.v.apply()
        with self.assertRaises(VibeError):
            self.v.run_explicit("main.py", "")
        self.assertIn("Works", self.v.run_explicit("main.py", "CONFERMO"))

    def test_natural_language_routes_to_generator(self):
        app = ReadyLinux(self.root / "programs")
        app.vibe.ai = self.ai
        self.ai.propose_project.return_value = json.dumps({"summary": "test", "files": [{"path": "main.py", "content": "print(1)"}]})
        with contextlib.redirect_stdout(io.StringIO()) as output:
            app.command("crea un gioco di indovinelli")
        self.assertIn("NON APPLICATA", output.getvalue())
        self.assertFalse((app.vibe.root / "progetto/main.py").exists())
        self.assertEqual(len(self.ai.propose_project.call_args.args), 3)

    def test_multiple_module_project_run(self):
        self.stage([{"path": "helper.py", "content": 'MESSAGE = "Modulo locale"\n'},
                    {"path": "main.py", "content": 'from helper import MESSAGE\nprint(MESSAGE)\n'}])
        self.v.apply()
        self.assertIn("Modulo locale", self.v.run_explicit("main.py", "CONFERMO"))

    def test_invalid_proposal_discards_older_proposal(self):
        self.stage([{"path": "main.py", "content": "x=1"}])
        self.assertIsNotNone(self.v.pending)
        with self.assertRaises(VibeError):
            self.v.stage_json(json.dumps({"files": [{"path": "../oops.py", "content": "bad"}]}))
        self.assertIsNone(self.v.pending)


if __name__ == "__main__":
    unittest.main()
