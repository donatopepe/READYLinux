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

    def test_rejects_missing_kernel_cmdline_before_qemu_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bindir = root / "bin"
            bindir.mkdir()
            image = root / "image.raw"
            image.write_bytes(b"verified image fixture")
            kernel = root / "kernel"
            kernel.write_bytes(b"kernel fixture")
            invocation_log = root / "invoked.log"
            for name in ("qemu-img", "qemu-system-x86_64"):
                stub = bindir / name
                stub.write_text("#!/bin/sh\\ntouch \\\"$INVOCATION_LOG\\\"\\n", encoding="utf-8")
                stub.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{self.fake_shell_path(bindir)}:/usr/bin:/bin",
                "READY_QEMU_KERNEL": self.fake_shell_path(kernel),
                "READY_QEMU_BIN": self.fake_shell_path(bindir / "qemu-system-x86_64"),
                "READY_QEMU_IMG": self.fake_shell_path(bindir / "qemu-img"),
                "READY_QEMU_APPEND": "",
                "INVOCATION_LOG": self.fake_shell_path(invocation_log),
            }
            result = self.run_script(image, hashlib.sha256(image.read_bytes()).hexdigest(), "pc", env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("set READY_QEMU_APPEND", result.stderr)
        self.assertFalse(invocation_log.exists(), "QEMU tools must not run without explicit kernel cmdline")

    def fake_shell_path(self, path):
        if os.name == "nt":
            result = subprocess.run(["bash", "-lc", "cygpath -u \"$1\"", "bash", str(path)], cwd=ROOT, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        return str(path)

    def test_verified_boot_uses_temporary_overlay_and_preserves_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            root_posix = self.fake_shell_path(root)
            bindir = root / "bin"
            bindir.mkdir()
            image = root / "base image.raw"
            image_bytes = b"fixture image bytes"
            image.write_bytes(image_bytes)
            kernel = root / "kernel Image"
            kernel.write_bytes(b"fixture kernel")
            args_log = root / "qemu-args.txt"
            overlay_log = root / "overlay-path.txt"
            qemu_img = bindir / "qemu-img"
            qemu_img.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$6\" > \"$OVERLAY_LOG\"\n: > \"$6\"\n",
                encoding="utf-8",
            )
            qemu = bindir / "qemu-system-x86_64"
            qemu.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$QEMU_ARGS_LOG\"\noverlay=$(cat \"$OVERLAY_LOG\")\n[ -f \"$overlay\" ] || exit 24\nexit 0\n",
                encoding="utf-8",
            )
            qemu_img.chmod(0o755)
            qemu.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{self.fake_shell_path(bindir)}:/usr/bin:/bin",
                "READY_QEMU_BIN": self.fake_shell_path(qemu),
                "READY_QEMU_IMG": self.fake_shell_path(qemu_img),
                "READY_QEMU_KERNEL": self.fake_shell_path(kernel),
                "READY_QEMU_APPEND": "console=ttyS0",
                "OVERLAY_LOG": self.fake_shell_path(overlay_log),
                "QEMU_ARGS_LOG": self.fake_shell_path(args_log),
            }
            result = self.run_script(image, hashlib.sha256(image_bytes).hexdigest(), "pc", env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            overlay_raw = overlay_log.read_text(encoding="utf-8").strip()
            overlay = root / Path(overlay_raw).name
            self.assertFalse(overlay.exists(), "temporary overlay should be removed after QEMU exits")
            self.assertEqual(image.read_bytes(), image_bytes, "base image must remain unchanged")
            qemu_args = args_log.read_text(encoding="utf-8")
            self.assertIn("-nic\nnone", qemu_args)
            self.assertIn("-monitor\nnone", qemu_args)
            self.assertIn("qcow2", qemu_args)

    def test_rejects_sha256_mismatch_before_invoking_qemu_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bindir = root / "bin"
            bindir.mkdir()
            image = root / "image.raw"
            original_image = b"trusted image bytes"
            image.write_bytes(original_image)
            kernel = root / "Image"
            kernel.write_bytes(b"kernel fixture")
            invocation_log = root / "invoked.log"
            qemu_img = bindir / "qemu-img"
            qemu_img.write_text("#!/bin/sh\\ntouch \\\"$INVOCATION_LOG\\\"\\n", encoding="utf-8")
            qemu = bindir / "qemu-system-x86_64"
            qemu.write_text("#!/bin/sh\\ntouch \\\"$INVOCATION_LOG\\\"\\n", encoding="utf-8")
            qemu_img.chmod(0o755)
            qemu.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{self.fake_shell_path(bindir)}:/usr/bin:/bin",
                "READY_QEMU_BIN": self.fake_shell_path(qemu),
                "READY_QEMU_IMG": self.fake_shell_path(qemu_img),
                "READY_QEMU_KERNEL": self.fake_shell_path(kernel),
                "READY_QEMU_APPEND": "console=ttyS0",
                "INVOCATION_LOG": self.fake_shell_path(invocation_log),
            }
            result = self.run_script(image, "0" * 64, "pc", env=env)
            self.assertEqual(result.returncode, 1)
            self.assertIn("SHA-256 mismatch", result.stderr)
            self.assertFalse(invocation_log.exists(), "qemu-img/qemu must not run for an unverified image")
            self.assertEqual(image.read_bytes(), original_image, "rejected image must remain unchanged")

    def test_qemu_nonzero_exit_propagates_and_cleans_temporary_overlay(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bindir = root / "bin"
            bindir.mkdir()
            image = root / "image with spaces.raw"
            image_bytes = b"base image stays intact"
            image.write_bytes(image_bytes)
            kernel = root / "Image"
            kernel.write_bytes(b"kernel fixture")
            overlay_log = root / "overlay-path.txt"
            qemu_img = bindir / "qemu-img"
            qemu_img.write_text("#!/bin/sh\nprintf '%s\\n' \"$6\" > \"$OVERLAY_LOG\"\n", encoding="utf-8")
            qemu = bindir / "qemu-system-x86_64"
            qemu.write_text("#!/bin/sh\nexit 23\n", encoding="utf-8")
            qemu_img.chmod(0o755)
            qemu.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{self.fake_shell_path(bindir)}:/usr/bin:/bin",
                "READY_QEMU_BIN": self.fake_shell_path(qemu),
                "READY_QEMU_IMG": self.fake_shell_path(qemu_img),
                "READY_QEMU_KERNEL": self.fake_shell_path(kernel),
                "READY_QEMU_APPEND": "console=ttyS0",
                "OVERLAY_LOG": self.fake_shell_path(overlay_log),
            }
            result = self.run_script(image, hashlib.sha256(image_bytes).hexdigest(), "q35", env=env)
            self.assertEqual(result.returncode, 23, result.stderr)
            overlay_raw = overlay_log.read_text(encoding="utf-8").strip()
            overlay = root / Path(overlay_raw).name
            self.assertFalse(overlay.exists(), "overlay should be removed even on QEMU failure")
            self.assertEqual(image.read_bytes(), image_bytes)

    def test_artifact_verifier_accepts_image_before_fake_qemu_boot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / "verified base image.wic"
            kernel = root / "matching kernel Image"
            image_bytes = b"verified image fixture"
            image.write_bytes(image_bytes)
            kernel.write_bytes(b"matching kernel fixture")
            digest = hashlib.sha256(image_bytes).hexdigest()
            verified = subprocess.run(["bash", str(ROOT / "scripts/verify-image-artifact.sh"), str(image), digest], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            overlay_log = root / "overlay.log"
            bindir = root / "bin"
            bindir.mkdir()
            qemu_img = bindir / "qemu-img"
            qemu_img.write_text("#!/bin/sh\nprintf '%s\\n' \"$6\" > \"$OVERLAY_LOG\"\n: > \"$6\"\n", encoding="utf-8")
            qemu = bindir / "qemu-system-x86_64"
            qemu.write_text("#!/bin/sh\noverlay=$(cat \"$OVERLAY_LOG\")\n[ -f \"$overlay\" ] || exit 24\nexit 0\n", encoding="utf-8")
            qemu_img.chmod(0o755)
            qemu.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{self.fake_shell_path(bindir)}:/usr/bin:/bin",
                "READY_QEMU_BIN": self.fake_shell_path(qemu),
                "READY_QEMU_IMG": self.fake_shell_path(qemu_img),
                "READY_QEMU_KERNEL": self.fake_shell_path(kernel),
                "READY_QEMU_APPEND": "console=ttyS0 root=/dev/vda",
                "OVERLAY_LOG": self.fake_shell_path(overlay_log),
            }
            booted = self.run_script(image, digest, "pc", env=env)
            self.assertEqual(booted.returncode, 0, booted.stderr)
            self.assertEqual(image.read_bytes(), image_bytes)

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
