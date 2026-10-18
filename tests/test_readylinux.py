import contextlib
import io
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from readylinux import ReadyLinux


class ReadyLinuxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = ReadyLinux(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def test_program_edit_run_save_load(self):
        self.app.command("10 print('CIAO')")
        self.app.command("20 for i in range(3):")
        self.app.command("30     print(i)")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.app.run()
        self.assertEqual(stdout.getvalue(), 'CIAO\n0\n1\n2\n')
        self.app.save("test")
        self.app.command("NEW")
        self.app.load("test")
        self.assertEqual(self.app.listing(), "10 print('CIAO')\n20 for i in range(3):\n30     print(i)")
        source = self.app.export("test").read_text(encoding="utf-8")
        self.assertEqual(source, "print('CIAO')\nfor i in range(3):\n    print(i)\n")

    def test_delete_line(self):
        self.app.command("10 x = 4")
        self.app.command("10")
        self.assertEqual(self.app.program, {})

    def test_reject_traversal(self):
        with self.assertRaises(ValueError):
            self.app.save("../foo")
        with self.assertRaises(ValueError):
            self.app.load("/tmp/demo")

    def test_immediate_python(self):
        self.app.command("x = 40")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.app.command("print(x + 2)")
        self.assertEqual(stdout.getvalue(), "42\n")

    def test_load_is_atomic_on_invalid_file(self):
        self.app.program[10] = "print('SAFE')"
        (Path(self.temp.name) / "broken.rdy").write_text("not a program\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.app.load("broken")
        self.assertEqual(self.app.program[10], "print('SAFE')")


if __name__ == "__main__":
    unittest.main()
