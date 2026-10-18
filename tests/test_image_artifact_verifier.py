import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify-image-artifact.sh"


class ImageArtifactVerifierTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(["bash", str(SCRIPT), *map(str, args)], cwd=ROOT, capture_output=True, text=True)

    def test_rejects_missing_and_empty_images(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.wic"
            empty = Path(temp) / "empty.wic"
            empty.write_bytes(b"")
            for path in (missing, empty):
                result = self.run_script(path, "0" * 64)
                self.assertEqual(result.returncode, 2)
                self.assertIn("existing non-empty regular file", result.stderr)

    def test_rejects_malformed_expected_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / "image.wic"
            image.write_bytes(b"fixture image bytes\n")
            for digest in ("", "0" * 63, "0" * 64 + "0", "g" * 64):
                result = self.run_script(image, digest)
                self.assertEqual(result.returncode, 2)
                self.assertIn("64 hexadecimal", result.stderr)

    def test_accepts_matching_digest_and_rejects_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / "image.wic"
            image.write_bytes(b"fixture image bytes\n")
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            valid = self.run_script(image, digest.upper())
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertIn(digest, valid.stdout.lower())
            mismatch = self.run_script(image, "0" * 64)
            self.assertEqual(mismatch.returncode, 1)
            self.assertIn("SHA-256 mismatch", mismatch.stderr)

    def test_script_shell_syntax(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
