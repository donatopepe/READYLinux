import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-yocto-env.sh"


def shell_pwd(path):
    result = subprocess.run(["bash", "-lc", "cd \"$1\" && pwd -P", "bash", str(path)], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def to_shell_path(path):
    if os.name == "nt":
        result = subprocess.run(["bash", "-lc", "cygpath -u \"$1\"", "bash", str(path)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return str(path)




class YoctoValidationScriptTests(unittest.TestCase):
    def test_script_is_shell_syntax_valid(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_fails_closed_without_bitbake_environment(self):
        result = subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=ROOT,
            env={"PATH": "/usr/bin:/bin"},
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("source the target build environment first", result.stderr)
        self.assertNotIn("bitbake -p", result.stdout)

    def run_with_builddir(self, builddir, *, with_bitbake=True, bitbake_exit=0, collection="readylinux", registered_layer=None, core_series="scarthgap styhead", image_fstypes="tar.bz2 ext4 wic"):
        temp_path = tempfile.TemporaryDirectory()
        bindir = Path(temp_path.name) / "bin"
        bindir.mkdir()
        if with_bitbake:
            fake = bindir / "bitbake"
            fake.write_text(f"#!/bin/sh\nprintf 'FAKE_BITBAKE %s %s\\n' \"$*\" \"$PWD\"\nexit {bitbake_exit}\n", encoding="utf-8")
            fake.chmod(0o755)
            layer_stub = bindir / "bitbake-layers"
            layer_path = registered_layer if registered_layer is not None else shell_pwd(ROOT / "meta-readylinux")
            stub_lines = [
                "#!/bin/sh",
                "printf 'layer path priority\n%s %s 8\n' '" + collection + "' '" + layer_path + "'",
                "",
            ]
            core_dir = Path(temp_path.name) / "core-meta"
            (core_dir / "conf").mkdir(parents=True, exist_ok=True)
            (core_dir / "conf/layer.conf").write_text(
                'LAYERSERIES_COMPAT_core = "' + core_series + '"' + chr(10), encoding="utf-8")
            stub_lines.insert(1, "printf 'core %s 5" + chr(92) + "n' '" + shell_pwd(core_dir) + "'")
            layer_stub.write_text(chr(10).join(stub_lines), encoding="utf-8")
            layer_stub.chmod(0o755)
            getvar = bindir / "bitbake-getvar"
            getvar.write_text(
                "#!/bin/sh" + chr(10) + "printf '%s" + chr(92) + "n' '" + image_fstypes + "'" + chr(10),
                encoding="utf-8",
            )
            getvar.chmod(0o755)
        env = {"PATH": f"{bindir}:/usr/bin:/bin", "BUILDDIR": to_shell_path(builddir)}
        return subprocess.run(["bash", str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True), temp_path

    def test_script_fails_when_bitbake_is_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            (builddir / "conf").mkdir()
            (builddir / "conf/bblayers.conf").write_text("", encoding="utf-8")
            (builddir / "conf/local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, with_bitbake=False)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("bitbake is not available", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_reports_the_matched_oe_series(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"' + chr(10), encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"' + chr(10), encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, core_series="styhead walnascar")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OE series: styhead", result.stdout)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_rejects_unlisted_oe_series(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"' + chr(10), encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"' + chr(10), encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, core_series="kirkstone")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
        self.assertIn("is not among LAYERSERIES_COMPAT_readylinux", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_rejects_misnamed_layer_collection(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"\n', encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, collection="wrongname")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("expected 'readylinux'", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_rejects_build_layers_reporting_a_different_path(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"\n', encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, registered_layer="/tmp/other-layer")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("does not report", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_rejects_non_ready_distro_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "poky"\n', encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn('requires DISTRO = "readylinux"', result.stderr)
        self.assertIn("poky", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_notes_missing_distro_but_still_validates_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("does not set DISTRO", result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_requires_wic_in_image_fstypes(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"' + chr(10), encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"' + chr(10), encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, image_fstypes="tar.bz2 ext4")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 6, result.stdout + result.stderr)
        self.assertIn("does not include wic", result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_reports_image_fstypes_when_wic_is_present(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"' + chr(10), encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"' + chr(10), encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, image_fstypes="ext4 wic")
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Image fstypes: ext4 wic", result.stdout)

    @unittest.skipIf(os.name == "nt", "POSIX path and grep semantics required")
    def test_script_accepts_ready_distro_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text('DISTRO = "readylinux"\n', encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("does not set DISTRO", result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_fails_when_build_configs_are_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            result, fake_root = self.run_with_builddir(Path(temp))
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    @unittest.skipIf(os.name == "nt", "temp directories on Windows are outside the WSL filesystem")
    def test_script_accepts_build_directory_with_spaces(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp) / "build tree with spaces"
            conf = builddir / "conf"
            conf.mkdir(parents=True)
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            expected_path = shell_pwd(builddir)
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Build directory: {expected_path}", result.stdout)
        self.assertIn(f"FAKE_BITBAKE -p {expected_path}", result.stdout)

    def test_script_accepts_symlinked_build_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actual = root / "build actual"
            conf = actual / "conf"
            conf.mkdir(parents=True)
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            alias = root / "build-link"
            alias.symlink_to(actual, target_is_directory=True)
            result, fake_root = self.run_with_builddir(alias)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_fails_when_layer_is_not_registered(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            (conf / "bblayers.conf").write_text("BBLAYERS = \\\"/some/other/layer\\\"\\n", encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 2)
        self.assertIn("add", result.stderr)
        self.assertNotIn("FAKE_BITBAKE", result.stdout)

    def test_script_runs_metadata_parse_only_after_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 0, result.stderr)
        announced_builddir = next(line.removeprefix("Build directory: ") for line in result.stdout.splitlines() if line.startswith("Build directory: "))
        self.assertTrue(announced_builddir)
        self.assertIn(f"FAKE_BITBAKE -p {announced_builddir}", result.stdout)

    def test_script_propagates_bitbake_parse_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            builddir = Path(temp)
            conf = builddir / "conf"
            conf.mkdir()
            layer_path = shell_pwd(ROOT / "meta-readylinux")
            (conf / "bblayers.conf").write_text(f'BBLAYERS += "{layer_path}"\n', encoding="utf-8")
            (conf / "local.conf").write_text("", encoding="utf-8")
            result, fake_root = self.run_with_builddir(builddir, bitbake_exit=37)
            self.addCleanup(fake_root.cleanup)
        self.assertEqual(result.returncode, 37)
        self.assertIn("FAKE_BITBAKE -p", result.stdout)

    def test_script_checks_build_confs_layer_registration_series_and_image_artifact(self):
        text = SCRIPT.read_text(encoding="utf-8")
        for check in (
            "BUILDDIR", "conf/bblayers.conf", "conf/local.conf", "bitbake",
            "bitbake-layers show-layers", "LAYERSERIES_COMPAT_core",
            "LAYERSERIES_COMPAT_readylinux", "bitbake -p", "bitbake-getvar",
            "IMAGE_FSTYPES", "Image fstypes:",
        ):
            self.assertIn(check, text)
        self.assertNotRegex(text, r"(?m)^\s*(?:git clone|curl|wget)\b")


if __name__ == "__main__":
    unittest.main()
