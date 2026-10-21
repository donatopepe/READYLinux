import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from basic import BasicError, BasicProgram
from readylinux import ReadyLinux


def prog(*lines):
    return chr(10).join(lines)


class BasicTests(unittest.TestCase):
    def run_program(self, source, **kwargs):
        program = BasicProgram(**kwargs)
        program.load_source(source)
        output = []
        variables = program.run(output=output.append)
        return output, variables

    def test_numbered_print_and_arithmetic(self):
        out, _ = self.run_program('10 PRINT "HELLO"\n20 PRINT 2+2')
        self.assertEqual(out, ["HELLO", "4"])

    def test_assignment_if_and_goto(self):
        out, vars_ = self.run_program('10 LET A=2\n20 IF A < 3 THEN 40\n30 PRINT "BAD"\n40 PRINT A')
        self.assertEqual(out, ["2"])
        self.assertEqual(vars_["A"], 2)

    def test_for_next_and_step(self):
        out, _ = self.run_program('10 FOR I=1 TO 3\n20 PRINT I\n30 NEXT I\n40 FOR J=4 TO 2 STEP -1\n50 PRINT J\n60 NEXT J')
        self.assertEqual(out, ["1", "2", "3", "4", "3", "2"])

    def test_gosub_return_and_input(self):
        p = BasicProgram()
        p.load_source('10 INPUT N\n20 GOSUB 50\n30 PRINT N\n40 END\n50 N=N+1\n60 RETURN')
        output = []
        p.run(output=output.append, input_fn=lambda _: "4")
        self.assertEqual(output, ["5"])

    def test_edit_delete_and_sorted_listing(self):
        p = BasicProgram()
        p.edit("20 PRINT 2")
        p.edit("10 PRINT 1")
        self.assertEqual(p.listing(), "10 PRINT 1\n20 PRINT 2")
        p.edit("10")
        self.assertEqual(p.listing(), "20 PRINT 2")

    def test_reject_duplicate_and_malformed_lines_atomically(self):
        p = BasicProgram()
        p.load_source("10 PRINT 1")
        with self.assertRaises(BasicError):
            p.load_source("10 PRINT 2\n10 PRINT 3")
        self.assertEqual(p.listing(), "10 PRINT 1")
        with self.assertRaises(BasicError):
            p.edit("PRINT 3")

    def test_reject_unsafe_expression_and_unknown_statement(self):
        with self.assertRaises(BasicError):
            self.run_program("10 PRINT __import__('os').system('echo unsafe')")
        with self.assertRaises(BasicError):
            self.run_program("10 POKE 1,2")

    def test_missing_jump_and_unmatched_return(self):
        with self.assertRaisesRegex(BasicError, "target line"):
            self.run_program("10 GOTO 999")
        with self.assertRaisesRegex(BasicError, "RETURN without"):
            self.run_program("10 RETURN")

    def test_rem_lines_are_ignored_and_end_stops_execution(self):
        out, _ = self.run_program(prog('10 REM ignored', '20 PRINT "A"', '30 END', '40 PRINT "B"'))
        self.assertEqual(out, ["A"])

    def test_stop_behaves_like_end(self):
        out, _ = self.run_program(prog('10 PRINT "A"', '20 STOP', '30 PRINT "B"'))
        self.assertEqual(out, ["A"])

    def test_boolean_operators_and_comparisons(self):
        out, _ = self.run_program(prog('10 PRINT 1 AND 0', '20 PRINT 1 OR 0', '30 PRINT NOT 0', '40 PRINT 2 <> 3'))
        self.assertEqual(out, ["False", "True", "True", "True"])

    def test_if_false_does_not_jump(self):
        out, _ = self.run_program(prog('10 LET A=5', '20 IF A < 3 THEN 40', '30 PRINT "STAY"', '40 PRINT "AFTER"'))
        self.assertEqual(out, ["STAY", "AFTER"])

    def test_string_variables_and_equality(self):
        out, vars_ = self.run_program(prog('10 LET S="AB"', '20 IF S = "AB" THEN 40', '30 PRINT "NO"', '40 PRINT S'))
        self.assertEqual(out, ["AB"])
        self.assertEqual(vars_["S"], "AB")

    def test_bare_print_emits_an_empty_line(self):
        out, _ = self.run_program(prog('10 PRINT', '20 PRINT "X"'))
        self.assertEqual(out, ["", "X"])

    def test_ready_basic_save_load_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            app = ReadyLinux(Path(temp))
            with patch("builtins.print"):
                app.command("BASIC")
                app.command("10 PRINT 42")
                app.command("SAVE sample")
                app.command("NEW")
                app.command("LOAD sample")
            self.assertEqual(app.basic.listing(), "10 PRINT 42")
            self.assertEqual((Path(temp) / "sample.bas").read_text(encoding="utf-8"), "10 PRINT 42\n")

    def test_step_limit_stops_infinite_loop(self):
        p = BasicProgram(step_limit=20)
        p.load_source("10 GOTO 10")
        with self.assertRaisesRegex(BasicError, "step limit"):
            p.run()

    def test_ready_commands_route_basic_without_changing_python(self):
        with tempfile.TemporaryDirectory() as temp:
            app = ReadyLinux(Path(temp))
            with patch("builtins.print") as mocked_print:
                app.command("BASIC")
                app.command('10 PRINT "BASIC OK"')
                app.command("20 END")
                app.command("RUN")
                app.command("STOP")
            printed = [call.args[0] for call in mocked_print.call_args_list]
            self.assertTrue(any("BASIC OK" in str(item) for item in printed))
            output = app.basic.listing()
            self.assertIn('10 PRINT "BASIC OK"', output)
            self.assertEqual(app.program, {})
            self.assertFalse(app.basic_mode)
            app.command("10 print('python legacy')")
            self.assertEqual(app.program[10], "print('python legacy')")


if __name__ == "__main__":
    unittest.main()
