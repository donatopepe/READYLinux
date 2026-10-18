import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/boot-image-qemu.sh"


class QemuBootHelperTests(unittest.TestCase):
    def run_script(self, *args, env=None):
        return subprocess.run(["bash", str(SCRIPT), *map(str, args)], cwd=ROOT, env=env, capture_output=True, text=True)

    def test_requires_explicit_image_hash_machine_and_kernel(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stderr)
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / "image.raw"
            kernel = Path(temp) / "kernel"
            image.write_bytes(b"fixture")
            kernel.write_bytes(b"fixture kernel")
            env = {**os.environ, "READY_QEMU_KERNEL": str(kernel), "READY_QEMU_APPEND": "console=ttyS0", "READY_QEMU_BIN": "missing-qemu", "READY_QEMU_IMG": "missing-qemu-img"}
            missing = self.run_script(image, hashlib.sha256(b"fixture").hexdigest(), "pc", env=env)
        self.assertEqual(missing.returncode, 2)
        self.assertIn("qemu-system-x86_64 and qemu-img are required", missing.stderr)

    def test_rejects_unapproved_machine_and_bad_digest_before_qemu(self):
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / "image.raw"
            kernel = Path(temp) / "kernel"
            image.write_bytes(b"fixture")
            kernel.write_bytes(b"fixture kernel")
            env = {**os.environ, "READY_QEMU_KERNEL": str(kernel), "READY_QEMU_APPEND": "console=ttyS0", "PATH": "/usr/bin:/bin"}
            bad_machine = self.run_script(image, "0" * 64, "unknown", env=env)
            self.assertEqual(bad_machine.returncode, 2)
            self.assertIn("unsupported machine", bad_machine.stderr)
            bad_hash = self.run_script(image, "bad", "pc", env=env)
            self.assertEqual(bad_hash.returncode, 2)
            self.assertIn("64 hexadecimal", bad_hash.stderr)

    def test_script_is_networkless_and_uses_copy_on_write_overlay(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for guard in ("-nic none", "-monitor none", "-kernel", "-append", "-no-reboot", "qemu_img_bin", "qcow2", "-drive"):
            self.assertIn(guard, text)
        self.assertNotRegex(text, r"(?m)^\s*(?:-netdev|hostfwd|virtfs|9p)")

    def test_script_shell_syntax(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
