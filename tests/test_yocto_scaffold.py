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
        install_match = re.search(r'IMAGE_INSTALL:append = "([^"]+)"', image)
        self.assertIsNotNone(install_match)
        self.assertEqual(set(install_match.group(1).split()), {"readylinux", "readylinux-console"})
        self.assertNotRegex(image, r"(?i)(?:gguf|safetensors|llama-server|https?://|SRC_URI)")
        console_recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('RDEPENDS:${PN} += "readylinux systemd"', console_recipe)

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
        recipe_dir = LAYER / "recipes-ready/readylinux"
        source_root = (recipe_dir / "../../../").resolve()
        self.assertEqual(source_root, ROOT.resolve())
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertTrue((source_root / source).is_file(), source)
        self.assertNotRegex(recipe, r"(?i)(?:gguf|safetensors|llama-server|https?://)")

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
        directives = {line.split("=", 1)[0]: line.split("=", 1)[1] for line in service.splitlines() if "=" in line and not line.startswith("#")}
        self.assertEqual(directives.get("User"), "ready")
        self.assertEqual(directives.get("Group"), "ready")
        self.assertEqual(directives.get("NoNewPrivileges"), "yes")
        self.assertEqual(directives.get("ProtectSystem"), "strict")
        self.assertEqual(directives.get("ProtectHome"), "yes")
        self.assertEqual(directives.get("PrivateTmp"), "yes")
        self.assertEqual(directives.get("ReadWritePaths"), "/var/lib/readylinux")
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        self.assertEqual(directives.get("StateDirectoryMode"), "0750")
        self.assertEqual(directives.get("UMask"), "0027")
        self.assertEqual(directives.get("Environment"), "XDG_DATA_HOME=/var/lib/readylinux")
        self.assertIn("--home-dir /var/lib/readylinux", recipe)
        self.assertIn("--gid ready", recipe)
        self.assertIn("/var/lib/readylinux/programs", directives.get("ExecStart", ""))
        self.assertNotIn("CapabilityBoundingSet", directives)
        self.assertNotIn("AmbientCapabilities", directives)
        self.assertNotEqual(directives.get("User"), "root")
        self.assertNotIn("RootDirectory", directives)
        self.assertNotIn("PrivateUsers", directives)
        self.assertNotEqual(directives.get("NoNewPrivileges"), "no")
        self.assertNotIn("ReadWriteDirectories", directives)
        self.assertNotIn("ReadOnlyPaths", directives)
        self.assertNotIn("PermissionsStartOnly", recipe)
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', recipe)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', recipe)
        self.assertIn("inherit systemd useradd allarch", recipe)
        self.assertIn('GROUPADD_PARAM:${PN} = "--system ready"', recipe)
        self.assertIn("USERADD_PARAM:${PN}", recipe)
        self.assertIn("ln -s /dev/null ${D}${sysconfdir}/systemd/system/getty@tty1.service", recipe)
        self.assertIn("${sysconfdir}/systemd/system/getty@tty1.service", recipe)
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("readylinux-console", image)

    def test_layer_docs_order_environment_layer_parse_and_build(self):
        for doc_path in (LAYER / "README.md", LAYER / "README.en.md"):
            doc = doc_path.read_text(encoding="utf-8")
            commands = ["source oe-init-build-env", "bitbake-layers add-layer", "bash scripts/validate-yocto-env.sh", "bitbake readylinux-image"]
            positions = [doc.index(command) for command in commands]
            self.assertEqual(positions, sorted(positions), f"command order in {doc_path.name}")
            self.assertIn("MACHINE", doc)

    def test_build_evidence_templates_include_required_provenance_and_results(self):
        docs = (
            ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.md",
            ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md",
        )
        required = ("Poky/OE-Core", "BitBake version", "MACHINE", "checksum", "QEMU", "getty@tty1", "Not verified")
        for path in docs:
            text = path.read_text(encoding="utf-8")
            for item in required:
                self.assertIn(item, text, f"{item} missing from {path.name}")
            self.assertIn("Run ID / UTC date:", text)
            self.assertIn("exact commit:", text)
            self.assertIn("SHA-256:", text)
            self.assertIn("[ ] Not verified / blocked", text)
            self.assertNotRegex(text, r"(?im)^(?:[A-Za-z0-9_-]+\s+){5,}[0-9a-f]{7,40}$")

    def test_build_evidence_templates_have_semantic_field_parity(self):
        it = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.md").read_text(encoding="utf-8")
        en = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md").read_text(encoding="utf-8")
        fields = (
            "Run ID / UTC date", "Host OS and architecture", "Poky/OE-Core",
            "Other layer", "READY Linux repository commit", "BitBake version",
            "Distro", "MACHINE", "Build directory", "bblayers.conf",
            "local.conf", "exit code", "build log", "Image artifact",
            "SHA-256", "QEMU version", "READY appears", "unprivileged",
            "/var/lib/readylinux", "getty@tty1", "BASIC smoke", "offline smoke",
        )
        for label in fields:
            self.assertIn(label, it, f"Italian template missing {label}")
            self.assertIn(label, en, f"English template missing {label}")

    def test_layer_docs_define_reproducibility_evidence(self):
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        for requirement in ("Poky/OE-Core commit", "MACHINE", "bitbake -p", "checksums", "QEMU"):
            self.assertIn(requirement, italian)
            self.assertIn(requirement, english)

    def test_layer_documentation_warns_build_not_verified(self):
        readme = (LAYER / "README.md").read_text(encoding="utf-8")
        self.assertIn("BitBake and QEMU unavailable", readme)
        self.assertIn("does not clone repositories or download source", readme)
        self.assertIn("does not provide a normal login prompt there", readme)


if __name__ == "__main__":
    unittest.main()
