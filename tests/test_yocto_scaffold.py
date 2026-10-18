import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYER = ROOT / "meta-readylinux"


class YoctoScaffoldTests(unittest.TestCase):
    def test_layer_collection_and_compatibility_are_declared(self):
        conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        self.assertIn('BBFILE_COLLECTIONS += "readylinux"', conf)
        self.assertIn('BBFILE_PATTERN_readylinux = "^${LAYERDIR}/"', conf)
        self.assertRegex(conf, r"LAYERSERIES_COMPAT_readylinux\s*=\s*\"[^\"]+\"")

    def test_image_extends_core_minimal_and_installs_runtime(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("require recipes-core/images/core-image-minimal.bb", image)
        self.assertIn('IMAGE_INSTALL:append = " readylinux readylinux-console"', image)

    def test_recipe_includes_runtime_sources_and_no_external_fetch(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertIn(f"file://{source}", recipe)
        self.assertNotRegex(recipe, r"(?m)^\s*(?:git|https?)://")
        self.assertIn('LICENSE = "MIT"', recipe)
        self.assertIn("exec python3 /usr/share/readylinux/readylinux.py", recipe)
        launcher = recipe.split("cat > ${D}${bindir}/readylinux <<'EOF'\n", 1)[1].split("\nEOF", 1)[0]
        self.assertNotIn("${datadir}", launcher)
        for dependency in ("python3-core", "python3-difflib", "python3-crypt", "python3-json", "python3-misc", "python3-netclient", "python3-shell"):
            self.assertIn(dependency, recipe)
        self.assertNotIn("python3-multiprocessing", recipe)
        self.assertNotIn("python3-io", recipe)
        # FILESEXTRAPATHS resolves from recipe dir: readylinux -> recipes-ready -> layer -> repo root.
        recipe_dir = LAYER / "recipes-ready/readylinux"
        source_root = (recipe_dir / "../../../").resolve()
        self.assertEqual(source_root, ROOT.resolve())
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertTrue((source_root / source).is_file(), source)

    def test_recipe_dependencies_cover_non_core_stdlib_imports(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        dependency_match = re.search(r'RDEPENDS:\$\{PN\}\s*\+=\s*"([^"]+)"', recipe)
        self.assertIsNotNone(dependency_match, "RDEPENDS missing from runtime recipe")
        declared = set(dependency_match.group(1).split())
        source_files = (ROOT / name for name in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"))
        stdlib = set()
        for source in source_files:
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    stdlib.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    stdlib.add(node.module.split(".")[0])
        local_modules = {"ai_local", "basic", "vibe", "__future__"}
        packaged = {"argparse": "python3-core", "code": "python3-core", "ast": "python3-core", "operator": "python3-core", "re": "python3-core", "sys": "python3-core", "traceback": "python3-core", "os": "python3-core", "shutil": "python3-core", "socket": "python3-core", "time": "python3-core", "dataclasses": "python3-core", "typing": "python3-core", "pathlib": "python3-core", "urllib": "python3-netclient", "subprocess": "python3-misc", "difflib": "python3-difflib", "hashlib": "python3-crypt", "json": "python3-json", "tempfile": "python3-misc"}
        unknown = stdlib - local_modules - set(packaged)
        self.assertFalse(unknown, f"Add package mapping for imports: {sorted(unknown)}")
        required = {packaged[module] for module in stdlib - local_modules}
        self.assertTrue(required.issubset(declared), f"Missing RDEPENDS: {sorted(required - declared)}")

    def test_console_service_starts_on_tty1_and_is_enabled(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn("ExecStart=/usr/bin/readylinux", service)
        self.assertIn("TTYPath=/dev/tty1", service)
        self.assertIn("User=ready", service)
        self.assertIn("ReadWritePaths=/var/lib/readylinux", service)
        self.assertIn("NoNewPrivileges=yes", service)
        self.assertIn("ProtectSystem=strict", service)
        self.assertIn("StateDirectory=readylinux", service)
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', recipe)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', recipe)
        self.assertIn("inherit systemd useradd allarch", recipe)
        self.assertIn('GROUPADD_PARAM:${PN} = "--system ready"', recipe)
        self.assertIn("USERADD_PARAM:${PN}", recipe)
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("readylinux-console", image)

    def test_layer_documentation_warns_build_not_verified(self):
        readme = (LAYER / "README.md").read_text(encoding="utf-8")
        self.assertIn("BitBake and QEMU unavailable", readme)
        self.assertIn("does not clone repositories or download source", readme)


if __name__ == "__main__":
    unittest.main()
