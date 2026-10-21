import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITALIAN = ROOT / "docs/BASIC.md"
ENGLISH = ROOT / "docs/BASIC.en.md"
INTERPRETER = ROOT / "basic.py"
CONSOLE = ROOT / "readylinux.py"
TOKEN = re.compile(r"`([A-Z]{2,7})")


def keywords(path):
    return set(TOKEN.findall(path.read_text(encoding="utf-8")))


def language_keywords(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("`LET`"):
            return set(TOKEN.findall(line))
    raise AssertionError(f"no implemented-language line found in {path.name}")


class BasicDocsTests(unittest.TestCase):
    def test_bilingual_docs_list_the_same_keywords(self):
        italian = keywords(ITALIAN)
        english = keywords(ENGLISH)
        self.assertTrue(italian)
        self.assertEqual(italian - english, set(), "keywords documented only in Italian")
        self.assertEqual(english - italian, set(), "keywords documented only in English")

    def test_documented_keywords_exist_in_the_interpreter(self):
        source = INTERPRETER.read_text(encoding="utf-8")
        for keyword in sorted(language_keywords(ITALIAN)):
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, source, f"{keyword} is documented but not handled by basic.py")

    def test_documented_console_commands_exist_in_the_console(self):
        console = CONSOLE.read_text(encoding="utf-8")
        for command in ("LIST", "RUN", "NEW", "HELP", "STOP", "SAVE", "LOAD", "EDIT"):
            with self.subTest(command=command):
                self.assertIn(f'"{command}"', console, f"{command} is documented but missing in readylinux.py")

    def test_both_docs_disclaim_full_commodore_compatibility(self):
        italian = ITALIAN.read_text(encoding="utf-8").lower()
        english = ENGLISH.read_text(encoding="utf-8").lower()
        self.assertRegex(italian, r"non garantisce compatibilit.{0,20}completa")
        self.assertRegex(english, r"not full commodore basic compatibility|not full")

    def test_both_docs_warn_that_the_allowlist_is_not_a_sandbox(self):
        italian = ITALIAN.read_text(encoding="utf-8").lower()
        english = ENGLISH.read_text(encoding="utf-8").lower()
        self.assertIn("sandbox", italian)
        self.assertIn("sandbox", english)
        self.assertRegex(italian, r"non.{0,20}una sandbox")
        self.assertRegex(english, r"not.{0,10}sandbox")


if __name__ == "__main__":
    unittest.main()
