import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYER = ROOT / "meta-readylinux"


class YoctoScaffoldTests(unittest.TestCase):
    def test_repository_ignore_rules_cover_generated_and_sensitive_runtime_files(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        for pattern in ("__pycache__/", "*.py[cod]", ".pi-loop.json.lock", "*.gguf"):
            self.assertIn(pattern, ignore)
        self.assertIn("*.zip", ignore)

    def test_layer_collection_and_compatibility_are_declared(self):
        conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        self.assertIn('BBFILE_COLLECTIONS += "readylinux"', conf)
        self.assertIn('BBFILE_PATTERN_readylinux = "^${LAYERDIR}/"', conf)
        self.assertRegex(conf, r"LAYERSERIES_COMPAT_readylinux\s*=\s*\"[^\"]+\"")

    def test_layer_metadata_and_recipes_use_modern_override_syntax(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        recipes = (
            LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb",
            LAYER / "recipes-ready/readylinux/readylinux_0.3.bb",
        )
        self.assertIn("LAYERSERIES_COMPAT_readylinux", layer_conf)
        for recipe_path in recipes:
            recipe = recipe_path.read_text(encoding="utf-8")
            self.assertNotRegex(recipe, r"(?m)^\\s*(?:RDEPENDS|FILES|SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE|FILESEXTRAPATHS)_[A-Za-z]\\w*\\s*[+:?]?=")
            self.assertNotRegex(recipe, r"(?m)^\\s*(?:RDEPENDS|FILES|SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE):[A-Za-z_]+\\s*=")
        self.assertIn("RDEPENDS:${PN}", recipes[0].read_text(encoding="utf-8"))
        self.assertIn("FILESEXTRAPATHS:prepend", recipes[1].read_text(encoding="utf-8"))

    def test_image_extends_core_minimal_and_installs_runtime(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("require recipes-core/images/core-image-minimal.bb", image)
        install_match = re.search(r'IMAGE_INSTALL:append = "([^"]+)"', image)
        self.assertIsNotNone(install_match)
        self.assertEqual(set(install_match.group(1).split()), {"readylinux", "readylinux-console"})
        self.assertNotRegex(image, r"(?i)(?:gguf|safetensors|llama-server|https?://|SRC_URI)")
        console_recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('RDEPENDS:${PN} += "readylinux systemd"', console_recipe)

    def test_readylinux_distro_is_opt_in_and_documented_for_builds(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        self.assertIn('DISTRO = "readylinux"', distro)
        self.assertIn('DISTRO_FEATURES:append = " systemd"', distro)
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertNotIn("DISTRO =", image)
        for readme in (italian, english):
            self.assertIn('DISTRO = "readylinux"', readme)
            self.assertIn('MACHINE = "<selected-bsp-machine>"', readme)

    def test_ready_distro_selects_systemd_without_forcing_service_runtime(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        service_recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('DISTRO_FEATURES:append = " systemd"', distro)
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertIn('inherit systemd useradd allarch', service_recipe)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', service_recipe)
        self.assertIn('RDEPENDS:${PN} += "readylinux systemd"', service_recipe)
        self.assertNotIn("DISTRO_FEATURES:remove", distro)

    def test_image_recipe_has_license_and_minimal_local_package_contract(self):
        image_path = LAYER / "recipes-core/images/readylinux-image.bb"
        image = image_path.read_text(encoding="utf-8")
        self.assertIn('LICENSE = "MIT"', image)
        self.assertIn("require recipes-core/images/core-image-minimal.bb", image)
        install_match = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^\"]+)"', image)
        self.assertIsNotNone(install_match)
        self.assertEqual(set(install_match.group(1).split()), {"readylinux", "readylinux-console"})
        self.assertNotRegex(image, r"(?i)(?:https?://|git://|AUTOREV|gguf|safetensors)")
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertIn('DISTRO_FEATURES:append = " systemd"', distro)

    def test_image_installs_every_custom_recipe_package_exactly_once(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        package_names = set()
        for recipe_path in LAYER.rglob("*.bb"):
            if recipe_path == LAYER / "recipes-core/images/readylinux-image.bb":
                continue
            if recipe_path.name.startswith("readylinux-") or recipe_path.parent.parent.name == "recipes-ready":
                match = re.search(r"PN\\s*=\\s*\"([^\"]+)\"", recipe_path.read_text(encoding="utf-8"))
                if match:
                    package_names.add(match.group(1))
                else:
                    package_names.add(recipe_path.name.split("_", 1)[0])
        install_match = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^"]+)"', image)
        self.assertIsNotNone(install_match)
        installed = install_match.group(1).split()
        self.assertEqual(len(installed), len(set(installed)), "IMAGE_INSTALL contains duplicate package entries")
        self.assertEqual(set(installed), package_names)

    def test_src_uri_local_source_extraction_ignores_non_local_tokens(self):
        samples = {
            'SRC_URI = "file://alpha.py file://dir/beta.patch https://example.invalid/file.tar.gz"': ["alpha.py", "dir/beta.patch"],
            'SRC_URI = "file://patch.diff;apply=yes file://archive.tar.gz;unpack=0"': ["patch.diff", "archive.tar.gz"],
            'SRC_URI = "\\\n file://one\\\n file://two\\\n"': ["one", "two"],
            'SRC_URI = "https://example.invalid/source.tar.gz"': [],
        }
        for assignment, expected in samples.items():
            match = re.search(r'(?m)^SRC_URI\s*=\s*"([^"]*)"', assignment)
            extracted = [token.split(";", 1)[0] for token in re.findall(r"file://([^\s\\]+)", match.group(1))] if match else []
            self.assertEqual(extracted, expected, assignment)

    def test_all_recipe_file_uri_sources_resolve_inside_repository(self):
        for recipe_path in sorted(LAYER.rglob("*.bb")):
            recipe = recipe_path.read_text(encoding="utf-8")
            src_uri_match = re.search(r'(?m)^SRC_URI\\s*=\\s*"([^"]*)"', recipe)
            sources = [token.split(";", 1)[0] for token in re.findall(r"file://([^\\s\\\\]+)", src_uri_match.group(1))] if src_uri_match else []
            search_roots = [recipe_path.parent, ROOT]
            prepend_match = re.search(r'FILESEXTRAPATHS:prepend\\s*:?=\\s*"([^\"]+)"', recipe)
            if prepend_match:
                relative = prepend_match.group(1).replace("${THISDIR}/", "")
                search_roots.insert(0, (recipe_path.parent / relative).resolve())
            for source in sources:
                self.assertTrue(any((base / source).is_file() for base in search_roots), f"{source} missing for {recipe_path.relative_to(ROOT)}")

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

    def test_license_checksum_is_consistent_across_local_recipes(self):
        recipes = (
            LAYER / "recipes-ready/readylinux/readylinux_0.3.bb",
            LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb",
        )
        checksum_pattern = r'LIC_FILES_CHKSUM\s*=\s*"file://\$\{COMMON_LICENSE_DIR\}/MIT;md5=([0-9a-f]{32})"'
        checksums = []
        for recipe_path in recipes:
            recipe = recipe_path.read_text(encoding="utf-8")
            self.assertIn('LICENSE = "MIT"', recipe)
            match = re.search(checksum_pattern, recipe)
            self.assertIsNotNone(match, recipe_path.name)
            checksums.append(match.group(1))
        self.assertEqual(len(set(checksums)), 1)
        self.assertEqual(checksums[0], "0835ade698e0bcf8506ecda2f7b4f302")

    def test_recipes_declare_license_provenance_and_runtime_dependencies(self):
        runtime = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        service = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        expected_license = 'LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"'
        for recipe in (runtime, service):
            self.assertIn('LICENSE = "MIT"', recipe)
            self.assertIn(expected_license, recipe)
        self.assertIn('RDEPENDS:${PN} += "readylinux systemd"', service)
        self.assertIn("USERADD_PARAM:${PN}", service)
        self.assertIn('GROUPADD_PARAM:${PN} = "--system ready"', service)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', service)
        self.assertNotIn("AUTOREV", runtime + service)
        self.assertNotRegex(runtime + service, r"(?m)^\\s*(?:git|https?)://")

    def test_runtime_recipe_copies_each_declared_local_source_to_packaged_destination(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        src_uri = re.search(r'(?m)^SRC_URI\s*=\s*"([^"]*)"', recipe)
        self.assertIsNotNone(src_uri)
        declared = {Path(item).name for item in re.findall(r"file://([^\s\\]+)", src_uri.group(1))}
        installed = set(re.findall(r"install -m 0644 \$\{WORKDIR\}/([^\s]+) \$\{D\}\$\{datadir\}/readylinux/([^\s]+)", recipe))
        self.assertEqual({source for source, _destination in installed}, declared)
        self.assertEqual({destination for _source, destination in installed}, declared)
        for basename in declared:
            self.assertIn(f"{basename} ", recipe)
        self.assertIn('FILES:${PN} += "${datadir}/readylinux ${bindir}/readylinux"', recipe)

    def test_recipe_installed_paths_are_covered_by_package_files(self):
        runtime = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        console = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        for installed_path in ("${datadir}/readylinux", "${bindir}/readylinux"):
            self.assertIn(installed_path, runtime)
            self.assertIn(installed_path, runtime.split("FILES:${PN} +=", 1)[1])
        for installed_path in ("${systemd_system_unitdir}/readylinux-console.service", "${sysconfdir}/systemd/system/getty@tty1.service"):
            self.assertIn(installed_path, console)
            self.assertIn(installed_path, console.split("FILES:${PN} +=", 1)[1])
        self.assertIn("ln -s /dev/null", console)
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', console)

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
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        image_install = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^"]+)"', image)
        self.assertIsNotNone(image_install)
        self.assertTrue({"readylinux", "readylinux-console"}.issubset(set(image_install.group(1).split())))

    def test_service_user_group_and_state_directory_contract_match_recipe(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        user = directives.get("User")
        group = directives.get("Group")
        self.assertTrue(user)
        self.assertTrue(group)
        useradd = re.search(r'USERADD_PARAM:\$\{PN\}\s*=\s*"([^"]+)"', recipe)
        groupadd = re.search(r'GROUPADD_PARAM:\$\{PN\}\s*=\s*"([^"]+)"', recipe)
        self.assertIsNotNone(useradd)
        self.assertIsNotNone(groupadd)
        self.assertIn(f" {user}", useradd.group(1))
        self.assertIn(f"--gid {group}", useradd.group(1))
        self.assertIn(f" {group}", groupadd.group(1))
        state_directory = directives.get("StateDirectory", "")
        self.assertTrue(state_directory)
        self.assertIn(f"{state_directory}", directives.get("Environment", ""))
        self.assertEqual(directives.get("StateDirectoryMode"), "0750")

    def test_systemd_writable_paths_are_scoped_to_persistent_state_directory(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        self.assertEqual(directives.get("ReadWritePaths"), "/var/lib/readylinux")
        self.assertEqual(directives.get("Environment"), "XDG_DATA_HOME=/var/lib/readylinux")
        for forbidden in ("/home", "/etc", "/usr", "/opt"):
            self.assertNotIn(forbidden, directives.get("ReadWritePaths", ""))

    def test_systemd_service_hardening_is_fully_described_in_bilingual_readmes(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        readmes = (
            (LAYER / "README.md").read_text(encoding="utf-8"),
            (LAYER / "README.en.md").read_text(encoding="utf-8"),
        )
        documented_claims = (
            "NoNewPrivileges", "private tmp", "protected home/system/clock/kernel settings",
            "restricted SUID/SGID", "ready", "getty@tty1.service",
        )
        for claim in documented_claims:
            self.assertIn(claim.lower(), " ".join(readmes).lower())
        for directive in (
            "NoNewPrivileges=yes", "PrivateTmp=yes", "ProtectHome=yes", "ProtectSystem=strict",
            "ProtectClock=yes", "ProtectKernelLogs=yes", "ProtectControlGroups=yes",
            "ProtectKernelModules=yes", "ProtectKernelTunables=yes", "ProtectHostname=yes",
            "RestrictSUIDSGID=yes", "LockPersonality=yes", "RemoveIPC=yes",
        ):
            self.assertIn(directive, service)

    def test_console_service_starts_on_tty1_and_is_enabled(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn("ExecStart=/usr/bin/readylinux", service)
        self.assertIn("TTYPath=/dev/tty1", service)
        self.assertIn("User=ready", service)
        self.assertIn("ReadWritePaths=/var/lib/readylinux", service)
        self.assertIn("NoNewPrivileges=yes", service)
        self.assertIn("ProtectSystem=strict", service)
        self.assertIn("ProtectClock=yes", service)
        self.assertIn("ProtectKernelLogs=yes", service)
        self.assertIn("ProtectControlGroups=yes", service)
        self.assertIn("ProtectKernelModules=yes", service)
        self.assertIn("ProtectKernelTunables=yes", service)
        self.assertIn("ProtectHostname=yes", service)
        self.assertIn("RestrictSUIDSGID=yes", service)
        self.assertIn("LockPersonality=yes", service)
        self.assertIn("RemoveIPC=yes", service)
        self.assertIn("StateDirectory=readylinux", service)
        directives = {line.split("=", 1)[0]: line.split("=", 1)[1] for line in service.splitlines() if "=" in line and not line.startswith("#")}
        self.assertEqual(directives.get("User"), "ready")
        self.assertEqual(directives.get("Group"), "ready")
        self.assertEqual(directives.get("NoNewPrivileges"), "yes")
        self.assertEqual(directives.get("ProtectSystem"), "strict")
        for key in ("ProtectClock", "ProtectKernelLogs", "ProtectControlGroups", "ProtectKernelModules", "ProtectKernelTunables", "ProtectHostname", "RestrictSUIDSGID", "LockPersonality", "RemoveIPC"):
            self.assertEqual(directives.get(key), "yes", key)
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
        self.assertNotIn("AmbientCapabilities", directives)
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
        self.assertEqual(service.splitlines().count("ExecStart=/usr/bin/readylinux --workspace /var/lib/readylinux/programs"), 1)
        self.assertIn("${sysconfdir}/systemd/system/getty@tty1.service", recipe)
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("readylinux-console", image)

    def test_layer_docs_package_and_install_ownership_directions_match_recipe(self):
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('RDEPENDS:${PN} += "readylinux systemd"', recipe)
        for docs in (italian, english):
            self.assertIn("readylinux-console", docs)
            self.assertIn("getty@tty1.service", docs)
            self.assertIn("ready", docs)
        self.assertIn('FILES:${PN} += "${systemd_system_unitdir}/readylinux-console.service ${sysconfdir}/systemd/system/getty@tty1.service"', recipe)

    def test_layer_docs_make_distro_machine_and_cached_sources_requirements_explicit(self):
        for doc_path in (LAYER / "README.md", LAYER / "README.en.md"):
            doc = doc_path.read_text(encoding="utf-8")
            self.assertIn('DISTRO = "readylinux"', doc)
            self.assertIn('MACHINE = "<selected-bsp-machine>"', doc)
            self.assertIn("release series", doc.lower())
            self.assertTrue("cached" in doc.lower() or "cache" in doc.lower())
            self.assertLess(doc.index("DISTRO ="), doc.index("bash scripts/validate-yocto-env.sh"))

    def test_layer_docs_order_environment_layer_parse_and_build(self):
        for doc_path in (LAYER / "README.md", LAYER / "README.en.md"):
            doc = doc_path.read_text(encoding="utf-8")
            commands = ["source oe-init-build-env", "bitbake-layers add-layer", "bash scripts/validate-yocto-env.sh", "bitbake readylinux-image", "bash scripts/verify-image-artifact.sh", "bash scripts/boot-image-qemu.sh"]
            positions = [doc.index(command) for command in commands]
            self.assertEqual(positions, sorted(positions), f"command order in {doc_path.name}")
            self.assertIn("MACHINE", doc)

    def test_build_evidence_schema_is_valid_json_with_audit_fields(self):
        schema_path = ROOT / "docs/YOCTO_BUILD_EVIDENCE.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["type"], "object")
        self.assertFalse(schema["additionalProperties"])
        for section in ("identity", "environment", "image", "boot", "verdict"):
            self.assertIn(section, schema["required"])
            self.assertIn(section, schema["properties"])
        self.assertIn("readylinux_commit", schema["properties"]["identity"]["properties"])
        self.assertIn("sha256", schema["properties"]["image"]["properties"])
        props = schema["properties"]
        self.assertEqual(props["identity"]["properties"]["poky_commit"]["pattern"], "^[0-9a-fA-F]{40}$")
        self.assertEqual(props["environment"]["properties"]["local_conf_sha256"]["pattern"], "^[0-9a-fA-F]{64}$")
        self.assertEqual(props["image"]["properties"]["source_cache_state"]["enum"], ["cached", "fetched", "unknown", "not-built"])
        self.assertEqual(props["boot"]["properties"]["status"]["enum"], ["passed", "failed", "not-run"])
        self.assertEqual(props["verdict"]["enum"], ["reproducible-and-booted", "built-not-booted", "failed", "not-verified"])
        example = json.loads((ROOT / "docs/YOCTO_BUILD_EVIDENCE.example.json").read_text(encoding="utf-8"))
        self.assertEqual(set(example), set(schema["required"]))
        self.assertEqual(example["run_id"], "EXAMPLE-NOT-A-REAL-BUILD")
        self.assertEqual(example["identity"]["host_os"], "UNRECORDED")
        self.assertEqual(example["identity"]["machine"], "UNSELECTED")
        self.assertEqual(example["identity"]["bitbake_version"], "NOT-RUN")
        self.assertEqual(example["identity"]["poky_commit"], "0" * 40)
        self.assertEqual(example["environment"]["bblayers_conf_sha256"], "0" * 64)
        self.assertEqual(example["environment"]["local_conf_sha256"], "0" * 64)
        self.assertEqual(example["image"]["sha256"], None)
        self.assertEqual(example["environment"]["parse_log"], "NOT-RUN")
        self.assertTrue(any("Example only" in note for note in example["deviations"]))
        self.assertEqual(example["verdict"], "not-verified")
        serialized_example = json.dumps(example)
        self.assertNotIn("password=", serialized_example.lower())
        self.assertNotIn("token=", serialized_example.lower())
        self.assertNotIn("BEGIN PRIVATE KEY", serialized_example)
        self.assertIsNone(example["environment"]["parse_exit_code"])
        self.assertEqual(example["environment"]["parse_log"], "NOT-RUN")
        self.assertEqual(example["image"]["source_cache_state"], "not-built")
        self.assertIsNone(example["image"]["exit_code"])
        self.assertEqual(example["boot"]["status"], "not-run")
        self.assertIsNone(example["image"]["sha256"])
        for section in ("identity", "environment", "image", "boot"):
            schema_section = schema["properties"][section]
            self.assertEqual(set(example[section]), set(schema_section["properties"]))
            self.assertTrue(set(schema_section["required"]).issubset(example[section]))
        self.assertRegex(example["identity"]["poky_commit"], schema["properties"]["identity"]["properties"]["poky_commit"]["pattern"])
        self.assertRegex(example["environment"]["local_conf_sha256"], schema["properties"]["environment"]["properties"]["local_conf_sha256"]["pattern"])
        for section, key in (("image", "source_cache_state"), ("boot", "status"), ("verdict", None)):
            value = example[section] if key is None else example[section][key]
            enum = schema["properties"][section]["enum"] if key is None else schema["properties"][section]["properties"][key]["enum"]
            self.assertIn(value, enum)
        self.assertEqual(len(example["identity"]["poky_commit"]), 40)
        self.assertTrue(all(char in "0123456789abcdef" for char in example["identity"]["poky_commit"]))
        self.assertEqual(len(example["environment"]["local_conf_sha256"]), 64)
        self.assertTrue(all(char in "0123456789abcdef" for char in example["environment"]["local_conf_sha256"]))
        self.assertEqual(example["image"]["exit_code"], None)
        self.assertEqual(example["boot"]["status"], "not-run")
        self.assertEqual(example["verdict"], "not-verified")
        if example["image"]["source_cache_state"] == "not-built":
            self.assertIsNone(example["image"]["exit_code"])
            self.assertIsNone(example["image"]["artifact_path"])
            self.assertIsNone(example["image"]["sha256"])
        if example["boot"]["status"] == "not-run":
            for field in ("ready_console", "unprivileged_service", "persistent_state", "getty_mask", "basic_smoke", "offline_smoke"):
                self.assertEqual(example["boot"][field], "not-run", field)

        malformed_hash = dict(example["identity"])
        malformed_hash["poky_commit"] = "abc"
        self.assertNotRegex(malformed_hash["poky_commit"], r"^[0-9a-fA-F]{40}$")
        self.assertNotIn("success", schema["properties"]["verdict"]["enum"])
        missing_deviations = dict(example)
        missing_deviations.pop("deviations")
        self.assertIn("deviations", schema["required"])
        self.assertNotEqual(set(missing_deviations), set(schema["required"]))

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
            self.assertIn("SHA-256", text)
            self.assertIn("sha256sum <artifact>", text)
            self.assertIn("never commit", text.lower())
            self.assertIn("[ ] Not verified / blocked", text)
            self.assertIn("redact secrets", text.lower())
            self.assertIn("attach credentials", text.lower())
            self.assertNotRegex(text, r"(?im)^(?:[A-Za-z0-9_-]+\s+){5,}[0-9a-f]{7,40}$")

    def test_build_evidence_templates_require_unique_append_only_run_records(self):
        for path in (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.md", ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("unique run id", text, path.name)
            self.assertIn("never overwrite", text, path.name)
            self.assertIn("new record", text, path.name)
            self.assertIn("referencing the earlier one", text, path.name)

    def test_build_evidence_templates_have_semantic_field_parity(self):
        it = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.md").read_text(encoding="utf-8")
        en = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md").read_text(encoding="utf-8")
        fields = (
            "Run ID / UTC date", "Host OS and architecture", "Poky/OE-Core",
            "Other layer", "READY Linux repository commit", "BitBake version",
            "Distro", "MACHINE", "Build directory", "bblayers.conf",
            "local.conf", "exit code", "build log", "Image artifact",
            "SHA-256", "QEMU version", "READY appears", "unprivileged", "systemd-analyze security",
            "/var/lib/readylinux", "getty@tty1", "BASIC smoke", "offline smoke",
        )
        for label in fields:
            self.assertIn(label, it, f"Italian template missing {label}")
            self.assertIn(label, en, f"English template missing {label}")

    def test_build_evidence_template_sections_match_in_order(self):
        it = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.md").read_text(encoding="utf-8")
        en = (ROOT / "docs/YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md").read_text(encoding="utf-8")
        sections = ("Identity", "Environment and parse", "Image build", "Boot and smoke checks", "Verdict")
        for template in (it, en):
            headings = [line.lstrip("# ").strip() for line in template.splitlines() if line.startswith("## ")]
            self.assertEqual(len(headings), len(sections))
            self.assertEqual(headings[0], sections[0])
            self.assertEqual(headings[2:], list(sections[2:]))
            self.assertIn("Environment", headings[1])
            self.assertIn("parse", headings[1])
            self.assertEqual(headings[-1], sections[-1])

    def test_layer_docs_define_reproducibility_evidence(self):
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        for requirement in ("Poky/OE-Core commit", "MACHINE", "bitbake -p", "checksums", "QEMU"):
            self.assertIn(requirement, italian)
            self.assertIn(requirement, english)

    def test_status_records_current_test_baseline_and_bitbake_limitation(self):
        italian = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            self.assertIn("**Verificato localmente**" if "Stato READY" in doc else "**Locally verified**", doc)
            self.assertTrue("FIFO" in doc or "host-probe" in doc.lower())
            self.assertIn("BitBake", doc)
            self.assertIn("QEMU", doc)
            self.assertIn(".pi-loop.json", doc)
            self.assertTrue("HEAD" in doc or "firing start" in doc.lower() or "all'inizio unità" in doc.lower())
            self.assertRegex(doc, r"(?m)\*\*Git\*\*:.*[0-9a-f]{7}")
            self.assertIn("e82e9b12b8b3c0d52d99b24cea78fa828b79a1e4", doc)

    def test_console_tty_reservation_and_getty_mask_are_explained_bilingually(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        readmes = (
            (LAYER / "README.md").read_text(encoding="utf-8"),
            (LAYER / "README.en.md").read_text(encoding="utf-8"),
        )
        self.assertIn("TTYPath=/dev/tty1", service)
        self.assertIn("StandardInput=tty", service)
        self.assertIn("getty@tty1.service", recipe)
        self.assertIn("/dev/null", recipe)
        for readme in readmes:
            self.assertIn("/dev/tty1", readme)
            self.assertIn("getty@tty1.service", readme)
            self.assertRegex(readme.lower(), r"(?:no|does not provide).{0,80}(?:login|prompt)|(?:nessun|non offre).{0,80}(?:login|prompt)")

    def test_status_docs_state_current_build_limits_and_host_prereqs(self):
        italian = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        for doc, localized_status in ((italian, "Non verificato"), (english, "Not verified")):
            self.assertIn("BitBake", doc)
            self.assertIn("QEMU", doc)
            self.assertIn(localized_status, doc)
        for doc in (italian, english):
            self.assertIn("Git", doc)
            self.assertIn(".pi-loop", doc)
        self.assertIn("systemd", italian.lower())
        self.assertIn("systemd", english.lower())

    def test_test_results_docs_report_test_commands_and_scope(self):
        italian = (ROOT / "docs/TEST_RESULTS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/TEST_RESULTS.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            self.assertIn("python -m unittest discover -s tests -v", doc)
            self.assertIn("compileall", doc)
            self.assertIn("bash -n", doc)
            self.assertIn("BitBake", doc)
            self.assertIn("QEMU", doc)
            self.assertIn("compileall", doc)
            self.assertIn("bash -n", doc)
            self.assertNotIn("real Yocto build passed", doc.lower())

    def test_systemd_security_observation_and_skip_are_reported_bilingually(self):
        italian = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        results_it = (ROOT / "docs/TEST_RESULTS.md").read_text(encoding="utf-8")
        results_en = (ROOT / "docs/TEST_RESULTS.en.md").read_text(encoding="utf-8")
        self.assertIn("security --offline", results_it)
        self.assertIn("security --offline", results_en)
        for doc in (results_it, results_en):
            self.assertIn("MEDIUM/6.7", doc)
            self.assertIn("UMask 0027", doc)

    def test_layer_documentation_warns_build_not_verified(self):
        readme = (LAYER / "README.md").read_text(encoding="utf-8")
        self.assertIn("BitBake and QEMU unavailable", readme)
        self.assertIn("does not clone repositories or download source", readme)
        self.assertIn("does not provide a normal login prompt there", readme)


if __name__ == "__main__":
    unittest.main()
