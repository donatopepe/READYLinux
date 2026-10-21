import ast
import json
import os
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
LAYER = ROOT / "meta-readylinux"


class YoctoScaffoldTests(unittest.TestCase):
    def test_image_installs_console_package_that_owns_tty1_getty_mask(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        console = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        image_install = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^"]+)"', image)
        self.assertIsNotNone(image_install)
        image_packages = set(image_install.group(1).split())

        mask_install = re.search(r"(?m)^\s*ln -s /dev/null \$\{D\}(\$\{sysconfdir\}/systemd/system/getty@tty1\.service)\s*$", console)
        self.assertIsNotNone(mask_install, "console recipe must install the tty1 getty mask")
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', console)
        self.assertEqual(image_packages, {"readylinux-runtime", "readylinux-console"})
        self.assertIn("readylinux-console", image_packages)
        self.assertIn(mask_install.group(1), console.split("FILES:${PN} +=", 1)[1])

    def test_layer_recipe_inventory_is_explicit_and_exact(self):
        expected = {
            "recipes-core/images/readylinux-image.bb",
            "recipes-core/readylinux/readylinux-console_0.1.bb",
            "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
        }
        actual = {path.relative_to(LAYER).as_posix() for path in LAYER.rglob("*.bb")}
        self.assertEqual(actual, expected)
        append_files = list(LAYER.rglob("*.bbappend"))
        self.assertFalse(append_files, "unexpected append files require explicit audit")
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        bbfiles = re.search(r'(?m)^BBFILES\s*\+=\s*"([^"]+)"$', layer_conf)
        self.assertIsNotNone(bbfiles)
        self.assertEqual(len([token for token in bbfiles.group(1).split() if token.endswith(".bbappend")]), 1)
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn('IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"', image)
        packaged = actual - {"recipes-core/images/readylinux-image.bb"}
        self.assertEqual(packaged, {
            "recipes-core/readylinux/readylinux-console_0.1.bb",
            "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
        })

    def test_layer_recipes_declare_shared_mit_license_and_runtime_dependencies(self):
        recipes = {
            path.relative_to(LAYER).as_posix(): path.read_text(encoding="utf-8")
            for path in LAYER.rglob("*.bb")
            if path.name != "readylinux-image.bb"
        }
        expected_recipe_paths = {
            "recipes-core/readylinux/readylinux-console_0.1.bb",
            "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
        }
        self.assertEqual(set(recipes), expected_recipe_paths)
        expected_license_checksum = 'LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"'
        for name, recipe in recipes.items():
            with self.subTest(recipe=name):
                self.assertIn('LICENSE = "MIT"', recipe)
                self.assertIn(expected_license_checksum, recipe)
                self.assertIn("RDEPENDS:${PN}", recipe)
        self.assertIn('RDEPENDS:${PN} += "readylinux-runtime systemd"', recipes["recipes-core/readylinux/readylinux-console_0.1.bb"])
        app_recipe = recipes["recipes-ready/readylinux/readylinux-runtime_0.3.bb"]
        for dependency in ("python3-core", "python3-json", "python3-netclient"):
            self.assertIn(dependency, app_recipe)
        app_sources = re.findall(r"(?m)^\s+file://([^\s\\]+)", app_recipe)
        self.assertEqual(set(app_sources), {"readylinux.py", "basic.py", "ai_local.py", "vibe.py"})
        for source in app_sources:
            self.assertTrue((ROOT / source).is_file(), f"recipe source missing: {source}")

    def test_tracked_scripts_keep_the_executable_bit(self):
        try:
            listing = subprocess.run(
                ["git", "ls-files", "-s", "scripts/", "install.sh", "setup-ai-cpu.sh"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError) as error:
            self.skipTest(f"git ls-files unavailable: {error}")
        entries = [line for line in listing.splitlines() if line.strip()]
        self.assertTrue(entries, "no tracked scripts found")
        for line in entries:
            mode, _object, _stage, path = line.split()
            with self.subTest(path=path):
                self.assertEqual(mode, "100755", f"{path} must be committed executable (git update-index --chmod=+x)")

    def test_critical_yocto_metadata_files_are_not_accidentally_executable(self):
        paths = (
            LAYER / "recipes-core/images/readylinux-image.bb",
            LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb",
            LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
            LAYER / "recipes-core/readylinux/readylinux-console.service",
            LAYER / "conf/layer.conf",
            LAYER / "conf/distro/readylinux.conf",
        )
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file(), "required Yocto source is missing")
                if os.name == "nt" or "/mnt/" in str(path).replace("\\", "/"):
                    continue
                self.assertFalse(os.access(path, os.X_OK), "data/metadata files must not gain executable mode")

    def test_scripts_and_yocto_sources_use_unix_line_endings(self):
        patterns = ("*.py", "scripts/*.sh", "scripts/*.py", "tests/*.py")
        candidates = [path for pattern in patterns for path in ROOT.glob(pattern)]
        candidates += list(LAYER.rglob("*.bb")) + list(LAYER.rglob("*.service")) + list(LAYER.rglob("*.conf"))
        self.assertTrue(candidates)
        for path in candidates:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertNotIn(bytes([13, 10]), path.read_bytes(), "CRLF breaks shell scripts on WSL/Linux")

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
            LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
        )
        self.assertIn("LAYERSERIES_COMPAT_readylinux", layer_conf)
        distro_conf = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        required_distro_features = re.search(r'(?m)^DISTRO_FEATURES:append\s*=\s*"([^"]+)"$', distro_conf)
        self.assertIsNotNone(required_distro_features)
        self.assertEqual(set(required_distro_features.group(1).split()), {"systemd", "usrmerge"})
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro_conf)
        recipe_tokens = "\n".join(recipe_path.read_text(encoding="utf-8") for recipe_path in recipes)
        self.assertNotRegex(recipe_tokens, r"(?m)^\s*(?:OVERRIDES|DISTRO_FEATURES|IMAGE_INSTALL)_(?:append|prepend|remove)\s*=")
        legacy_assignment = re.compile(
            r"(?m)^\s*(?:RDEPENDS|FILES|SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE|FILESEXTRAPATHS)_[A-Za-z]\w*\s*[+:?]?="
        )
        legacy_override = re.compile(
            r"(?m)^\s*(?:RDEPENDS|FILES|SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE):[A-Za-z_]+\s*="
        )
        legacy_src_uri = re.compile(r"(?m)^\s*SRC_URI_append\s*=")
        legacy_recipe_overrides = re.compile(r"(?m)^\s*(?:RDEPENDS|FILES|SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE):(?:append|prepend|remove)\s*=")
        for recipe_path in recipes:
            recipe = recipe_path.read_text(encoding="utf-8")
            self.assertIsNone(legacy_assignment.search(recipe), f"legacy underscore assignment in {recipe_path.name}")
            self.assertIsNone(legacy_override.search(recipe), f"override appears after variable name in {recipe_path.name}")
            self.assertIsNone(legacy_src_uri.search(recipe), f"legacy SRC_URI_append in {recipe_path.name}")
            self.assertIsNone(legacy_recipe_overrides.search(recipe), f"legacy override operator syntax in {recipe_path.name}")
        self.assertIn("RDEPENDS:${PN}", recipes[0].read_text(encoding="utf-8"))
        self.assertIn("FILESEXTRAPATHS:prepend", recipes[1].read_text(encoding="utf-8"))

    def test_image_recipe_installs_only_declared_runtime_packages(self):
        runtime_recipe = LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb"
        console_recipe = LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb"
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")

        image_install = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^"]+)"', image)
        self.assertIsNotNone(image_install)
        image_packages = set(image_install.group(1).split())
        runtime_package = runtime_recipe.name.split("_", 1)[0]
        console_package = console_recipe.name.split("_", 1)[0]
        declared_packages = {runtime_package, console_package}
        self.assertEqual(image_packages, declared_packages)
        self.assertEqual(len(image_install.group(1).split()), len(image_packages))
        for package in image_packages:
            self.assertIn(package, {runtime_recipe.name.split("_", 1)[0], console_recipe.name.split("_", 1)[0]})

    def test_image_extends_core_minimal_and_installs_runtime(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertIn("require recipes-core/images/core-image-minimal.bb", image)
        install_match = re.search(r'IMAGE_INSTALL:append = "([^"]+)"', image)
        self.assertIsNotNone(install_match)
        self.assertEqual(set(install_match.group(1).split()), {"readylinux-runtime", "readylinux-console"})
        self.assertNotRegex(image, r"(?i)(?:gguf|safetensors|llama-server|https?://|SRC_URI)")
        console_recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('RDEPENDS:${PN} += "readylinux-runtime systemd"', console_recipe)

    def test_host_preflight_report_is_part_of_historical_firing_evidence(self):
        italian = (ROOT / "docs/TEST_RESULTS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/TEST_RESULTS.en.md").read_text(encoding="utf-8")
        for report in (italian, english):
            with self.subTest(report=report):
                self.assertIn("check-yocto-host.sh", report)
                self.assertIn("INCOMPLETE", report)
                self.assertIn("19/19", report)
                self.assertIn("bitbake-layers", report)
                self.assertIn("BUILDDIR", report)
                self.assertIn("exit 1", report.lower())
                self.assertRegex(report, r"(?m)^- (?:Comandi|Commands):")

    def test_layer_release_compatibility_entries_are_unique_documented_and_not_claimed_verified(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        compatibility = re.search(r"(?m)^LAYERSERIES_COMPAT_readylinux = \"([^\"]+)\"$", layer_conf)
        self.assertIsNotNone(compatibility)
        supported = compatibility.group(1).split()
        self.assertTrue(supported)
        self.assertEqual(len(supported), len(set(supported)))
        self.assertNotRegex(compatibility.group(1), r"(?i)(master|latest|main)")
        self.assertTrue(all(re.fullmatch(r"[a-z][a-z0-9]+", token) for token in supported))
        self.assertEqual(len(supported), 4, "review and pin the candidate compatibility set explicitly")
        self.assertEqual(supported, ["scarthgap", "styhead", "walnascar", "wrynose"])
        self.assertEqual(supported, sorted(supported), "candidate compatibility series should remain in deterministic order")
        compatibility_comment = next(
            (line for line in layer_conf.splitlines() if "compatibility series" in line.lower()),
            "",
        )
        self.assertTrue(compatibility_comment, "series list needs comment explaining it is an unverified compatibility claim")
        self.assertTrue("not yet been verified" in compatibility_comment.lower() or "not yet verified" in compatibility_comment.lower())

        readmes = (
            ((LAYER / "README.md").read_text(encoding="utf-8"), (), ("release-pinned poky/oe-core",)),
            ((LAYER / "README.en.md").read_text(encoding="utf-8"), (), ("release-pinned poky/oe-core",)),
        )
        for readme, mentioned_series, required_phrases in readmes:
            with self.subTest(readme="English" if not mentioned_series else "Italian"):
                for phrase in required_phrases:
                    self.assertIn(phrase, readme.lower())
                for series in mentioned_series:
                    self.assertIn(series, readme)
                self.assertRegex(readme.lower(), r"(?:not tested|not been tested|not verified|non verificat)")

    def test_layer_metadata_discovers_only_expected_recipe_roots(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        bbfiles = re.search(r'(?m)^BBFILES\s*\+=\s*"([^"]+)"$', layer_conf)
        self.assertIsNotNone(bbfiles)
        patterns = bbfiles.group(1).split()
        self.assertEqual(patterns, [
            "${LAYERDIR}/recipes-*/*/*.bb",
            "${LAYERDIR}/recipes-*/*/*.bbappend",
        ])
        actual_recipes = {path.relative_to(LAYER).as_posix() for path in LAYER.rglob("*.bb")}
        expected_paths = {
            "recipes-core/images/readylinux-image.bb",
            "recipes-core/readylinux/readylinux-console_0.1.bb",
            "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
        }
        self.assertEqual(actual_recipes, expected_paths)
        self.assertEqual(len(actual_recipes), 3)
        recipe_roots = {"/".join(path.split("/")[:2]) for path in actual_recipes}
        self.assertEqual(recipe_roots, {"recipes-core/images", "recipes-core/readylinux", "recipes-ready/readylinux"})

    def test_layer_metadata_has_single_collection_pattern_and_priority(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        for assignment in (
            r"(?m)^BBFILE_COLLECTIONS\s*\+=",
            r"(?m)^BBFILE_PATTERN_readylinux\s*=",
            r"(?m)^BBFILE_PRIORITY_readylinux\s*=",
        ):
            with self.subTest(assignment=assignment):
                self.assertEqual(len(re.findall(assignment, layer_conf)), 1)
        self.assertIn('BBFILE_COLLECTIONS += "readylinux"', layer_conf)
        self.assertIn('BBFILE_PATTERN_readylinux = "^${LAYERDIR}/"', layer_conf)
        self.assertEqual(len(re.findall(r"(?m)^BBFILE_PRIORITY_readylinux\s*=", layer_conf)), 1)
        self.assertEqual(len(re.findall(r"(?m)^LAYERSERIES_COMPAT_readylinux\s*=", layer_conf)), 1)

    def test_layer_metadata_bbfiles_patterns_are_distinct_and_recipe_focused(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        assignment = re.search(r'(?m)^BBFILES\s*\+=\s*"([^"]+)"$', layer_conf)
        self.assertIsNotNone(assignment)
        patterns = assignment.group(1).split()
        self.assertEqual(len(patterns), 2)
        self.assertEqual(len(set(patterns)), 2, "duplicate BBFILES pattern")
        self.assertEqual(sum(pattern.endswith(".bb") for pattern in patterns), 1)
        self.assertEqual(sum(pattern.endswith(".bbappend") for pattern in patterns), 1)
        for pattern in patterns:
            self.assertTrue(pattern.startswith("${LAYERDIR}/recipes-"))
            relative = pattern.replace("${LAYERDIR}/", "")
            self.assertEqual(len(Path(relative).parts), 3, "BBFILES glob should cover exactly root/category/recipe")
        self.assertEqual(patterns[0].count("*"), 3)
        self.assertEqual(patterns[1].count("*"), 3)
        self.assertNotIn("conf/", " ".join(patterns), "BBFILES should not scan configuration directories")
        recipes = [path for path in LAYER.rglob("*.bb") if path.name != "readylinux-image.bb"]
        appends = list(LAYER.rglob("*.bbappend"))
        self.assertTrue(all(path.parent.parent.name.startswith("recipes-") for path in recipes))
        self.assertEqual(appends, [], "no append files are currently expected; adding one requires inventory review")

    def test_layer_metadata_declares_collection_pattern_priority_and_supported_series(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        self.assertIn('BBFILE_COLLECTIONS += "readylinux"', layer_conf)
        self.assertIn('BBFILE_PATTERN_readylinux = "^${LAYERDIR}/"', layer_conf)
        self.assertRegex(layer_conf, r"(?m)^BBFILE_PRIORITY_readylinux = \"[1-9][0-9]*\"$")

        compatibility = re.search(r"(?m)^LAYERSERIES_COMPAT_readylinux = \"([^\"]+)\"$", layer_conf)
        self.assertIsNotNone(compatibility)
        series = compatibility.group(1).split()
        self.assertGreaterEqual(len(series), 1)
        self.assertEqual(len(series), len(set(series)), "duplicate Yocto compatibility series")
        self.assertTrue(all(re.fullmatch(r"[a-z][a-z0-9]+", item) for item in series), "compatibility tokens must be literal lowercase series names")
        self.assertNotRegex(compatibility.group(1), r"(?i)(master|latest|main)")
        self.assertEqual(series, sorted(series), "compatibility list should use stable lexical order for review diffs")

    def test_readylinux_distro_is_opt_in_and_documented_for_builds(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        self.assertIn('DISTRO = "readylinux"', distro)
        self.assertIn('DISTRO_FEATURES:append = " systemd usrmerge"', distro)
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertIn("usrmerge", distro, "systemd recipe requires the usrmerge distro feature")
        self.assertNotIn("DISTRO =", image)
        for readme in (italian, english):
            self.assertIn('DISTRO = "readylinux"', readme)
            self.assertIn('MACHINE = "<selected-bsp-machine>"', readme)

    def test_layer_series_comments_and_readme_candidate_list_match_conf(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        compatibility = re.search(r"(?m)^LAYERSERIES_COMPAT_readylinux = \"([^\"]+)\"$", layer_conf)
        self.assertIsNotNone(compatibility)
        candidates = compatibility.group(1).split()
        readmes = ((LAYER / "README.md").read_text(encoding="utf-8"),
                   (LAYER / "README.en.md").read_text(encoding="utf-8"))
        for readme_path, readme in zip((LAYER / "README.md", LAYER / "README.en.md"), readmes):
            with self.subTest(readme=readme_path.name):
                for candidate in candidates:
                    self.assertIn(candidate, readme)
                self.assertIn("candidate series", readme.lower())
                self.assertIn("release-pinned `bitbake -p`", readme.lower())
                self.assertRegex(readme.lower(), r"(?:has|have) not yet been verified")
                self.assertIn("LAYERSERIES_COMPAT_readylinux", readme)
                self.assertIn("conf/layer.conf", readme)

    def test_distro_feature_append_preserves_defaults_and_selects_systemd_init(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        feature_append = re.search(r'(?m)^DISTRO_FEATURES:append\s*=\s*"([^"]+)"$', distro)
        init_manager = re.search(r'(?m)^VIRTUAL-RUNTIME_init_manager\s*=\s*"([^"]+)"$', distro)
        self.assertIsNotNone(feature_append)
        self.assertIsNotNone(init_manager)
        features = feature_append.group(1).split()
        self.assertIn("systemd", features)
        self.assertNotIn("DISTRO_FEATURES:remove", distro)
        self.assertEqual(init_manager.group(1), "systemd")
        self.assertIn('DISTRO = "readylinux"', distro)
        self.assertNotIn('DISTRO = "readylinux"', (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8"))

    def test_distro_requires_poky_base_and_has_no_floating_requirements(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        self.assertRegex(distro, r"(?m)^require conf/distro/poky\.conf$")
        requires = re.findall(r"(?m)^(?:require|include)\s+(.+)$", distro)
        self.assertEqual(requires, ["conf/distro/poky.conf"])
        self.assertNotRegex(distro, r"(?i)(?:https?://|git://|AUTOREV|\bmaster\b|\blatest\b)")
        self.assertEqual(len(re.findall(r"(?m)^DISTRO = ", distro)), 1)

    def test_generic_distro_does_not_pin_a_machine_or_bsp(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        self.assertNotRegex(distro, r"(?m)^\s*MACHINE\s*[:+?]?=")
        self.assertNotRegex(distro, r"(?im)^\s*(?:require|include)\s+conf/machine/")
        for readme_path in (LAYER / "README.md", LAYER / "README.en.md"):
            readme = readme_path.read_text(encoding="utf-8")
            with self.subTest(readme=readme_path.name):
                self.assertIn('MACHINE = "<selected-bsp-machine>"', readme)
                self.assertIn("selected", readme.lower())

    def test_distro_metadata_key_order_is_stable_and_features_append_after_identity(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        identity_keys = ["DISTRO", "DISTRO_NAME", "DISTRO_VERSION"]
        identity_lines = []
        for key in identity_keys:
            match = re.search(rf"(?m)^{re.escape(key)}\s*=", distro)
            self.assertIsNotNone(match, f"missing distro key: {key}")
            identity_lines.append(match.start())
        self.assertEqual(identity_lines, sorted(identity_lines), "distro identity metadata should be grouped in stable order")
        feature_line = re.search(r"(?m)^DISTRO_FEATURES:append\s*=", distro)
        init_line = re.search(r"(?m)^VIRTUAL-RUNTIME_init_manager\s*=", distro)
        self.assertIsNotNone(feature_line)
        self.assertIsNotNone(init_line)
        self.assertGreater(feature_line.start(), identity_lines[-1])
        self.assertLess(feature_line.start(), init_line.start())

    def test_distro_identity_metadata_is_explicit_and_cpu_first(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        expected_settings = {
            "DISTRO": "readylinux",
            "DISTRO_NAME": "READY Linux",
            "DISTRO_VERSION": "0.3-dev",
            "VIRTUAL-RUNTIME_init_manager": "systemd",
        }
        settings = {
            match.group(1): match.group(2)
            for line in distro.splitlines()
            if (match := re.match(r'^([A-Za-z][A-Za-z0-9_-]*)\s*=\s*"([^"]*)"$', line))
        }
        for key, value in expected_settings.items():
            self.assertEqual(settings.get(key), value, key)
        self.assertIn("CPU-first", distro)
        self.assertIn("No AI model weights", distro)
        self.assertNotRegex(distro, r"(?i)(?:https?://|git://|AUTOREV|gguf|safetensors)")

    def test_ready_distro_selects_systemd_without_forcing_service_runtime(self):
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        service_recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn('DISTRO_FEATURES:append = " systemd usrmerge"', distro)
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertIn('inherit systemd useradd allarch', service_recipe)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', service_recipe)
        self.assertIn('RDEPENDS:${PN} += "readylinux-runtime systemd"', service_recipe)
        self.assertNotIn("DISTRO_FEATURES:remove", distro)

    def test_image_recipe_summary_identifies_the_ready_distribution(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        summary = re.search(r'(?m)^SUMMARY\s*=\s*"([^"]+)"$', image)
        self.assertIsNotNone(summary)
        self.assertIn("READY Linux", summary.group(1))
        self.assertEqual(len(re.findall(r"(?m)^SUMMARY\s*=", image)), 1)

    def test_image_recipe_modern_image_install_override_has_expected_order_and_scope(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        install_line = re.search(r'(?m)^IMAGE_INSTALL:append\s*=\s*"([^"]+)"$', image)
        self.assertIsNotNone(install_line)
        self.assertEqual(install_line.group(1).split(), ["readylinux-runtime", "readylinux-console"])
        self.assertNotRegex(image, r"(?m)^\s*IMAGE_INSTALL_(?:append|prepend|remove)\s*=")
        self.assertEqual(len(re.findall(r"(?m)^IMAGE_INSTALL:append\s*=", image)), 1)

    def test_image_recipe_declares_exactly_one_image_install_override(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        assignments = re.findall(r"(?m)^([A-Z][A-Z0-9_]*(?::[A-Za-z0-9_-]+)?)\s*[:+?]?=", image)
        self.assertEqual(assignments.count("IMAGE_INSTALL:append"), 1)
        self.assertEqual(assignments.count("SUMMARY"), 1)
        self.assertEqual(assignments.count("LICENSE"), 1)
        self.assertNotIn("IMAGE_INSTALL", assignments)

    def test_image_recipe_has_license_and_minimal_local_package_contract(self):
        image_path = LAYER / "recipes-core/images/readylinux-image.bb"
        image = image_path.read_text(encoding="utf-8")
        self.assertIn('LICENSE = "MIT"', image)
        self.assertIn("require recipes-core/images/core-image-minimal.bb", image)
        install_match = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^\"]+)"', image)
        self.assertIsNotNone(install_match)
        self.assertEqual(set(install_match.group(1).split()), {"readylinux-runtime", "readylinux-console"})
        self.assertNotRegex(image, r"(?i)(?:https?://|git://|AUTOREV|gguf|safetensors)")
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        self.assertIn('VIRTUAL-RUNTIME_init_manager = "systemd"', distro)
        self.assertIn('DISTRO_FEATURES:append = " systemd usrmerge"', distro)

    def test_image_recipe_produces_the_documented_wic_artifact(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        fstypes = re.findall(r"(?m)^IMAGE\w*FSTYPES[^=]*=", image)
        self.assertEqual(len(fstypes), 1, image)
        self.assertIn('IMAGE_FSTYPES:append = " wic"', image)
        for readme in ((LAYER / "README.md"), (LAYER / "README.en.md")):
            text = readme.read_text(encoding="utf-8")
            self.assertIn(".wic", text)
            self.assertIn("IMAGE_FSTYPES", text)

    def test_image_recipe_extends_minimal_and_does_not_select_target_policy(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertRegex(image, r"(?m)^require recipes-core/images/core-image-minimal\.bb$")
        self.assertRegex(image, r'(?m)^IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"$')
        self.assertEqual(len(re.findall(r"(?m)^require ", image)), 1)
        self.assertNotRegex(image, r"(?m)^\s*(?:DISTRO|MACHINE)\s*=")
        self.assertNotRegex(image, r"(?m)^IMAGE_INSTALL_(?:append|remove|prepend)\s*=")

    def test_image_recipe_override_syntax_is_modern_and_not_legacy(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertRegex(image, r'(?m)^IMAGE_INSTALL:append\s*=\s*"[^\"]+"$')
        self.assertNotRegex(image, r"(?m)^\s*(?:IMAGE_INSTALL|DISTRO_FEATURES|OVERRIDES)_(?:append|prepend|remove)\s*=")
        self.assertEqual(len(re.findall(r"(?m)^IMAGE_INSTALL:append\s*=", image)), 1)

    def test_image_recipe_package_list_has_no_whitespace_duplicate_artifacts(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        install_match = re.search(r'(?m)^IMAGE_INSTALL:append\s*=\s*"([^\"]*)"$', image)
        self.assertIsNotNone(install_match)
        entries = install_match.group(1).split()
        self.assertTrue(entries, "image must install at least one package")
        self.assertEqual(len(entries), len(set(entries)), "duplicate image package")
        self.assertEqual(entries, ["readylinux-runtime", "readylinux-console"])
        self.assertFalse(any(entry != entry.strip() for entry in entries))

    def test_image_recipe_installs_exactly_the_expected_packages_in_declared_order(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        install_match = re.search(r'(?m)^IMAGE_INSTALL:append\s*=\s*"([^"]+)"$', image)
        self.assertIsNotNone(install_match)
        entries = install_match.group(1).split()
        self.assertEqual(entries, ["readylinux-runtime", "readylinux-console"])
        self.assertEqual(entries, list(dict.fromkeys(entries)), "IMAGE_INSTALL package ordering has duplicates")
        self.assertEqual(image.count("IMAGE_INSTALL:append"), 1)
        self.assertNotIn('IMAGE_INSTALL:append = " readylinux-runtime readylinux-console readylinux-runtime"', image)
        self.assertEqual(len([token for token in entries if token == "readylinux-runtime"]), 1)
        self.assertEqual(len([token for token in entries if token == "readylinux-console"]), 1)

    def test_image_recipe_whitespace_and_recipe_line_endings_are_stable(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        runtime = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        service = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        for name, content in (("image", image), ("runtime", runtime), ("service", service)):
            with self.subTest(recipe=name):
                self.assertEqual(content, content.rstrip() + "\n", "recipe should end in one newline")
                self.assertFalse(any(line.rstrip() != line for line in content.splitlines()), "recipe has trailing whitespace")
                self.assertNotIn("\t", content, "recipe should use spaces, not tab indentation")

    def test_image_recipe_rejects_legacy_image_install_override_assignment(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        self.assertRegex(image, r"(?m)^IMAGE_INSTALL:append\s*=")
        self.assertNotRegex(image, r"(?m)^\s*IMAGE_INSTALL_(?:append|prepend|remove)\s*=")
        self.assertEqual(len(re.findall(r"(?m)^IMAGE_INSTALL:append\s*=", image)), 1)

    def test_image_recipe_has_one_summary_license_and_minimal_image_base(self):
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        summary = re.findall(r"(?m)^SUMMARY\s*=", image)
        licenses = re.findall(r"(?m)^LICENSE\s*=", image)
        base_includes = re.findall(r"(?m)^require\s+recipes-core/images/core-image-minimal\.bb\s*$", image)
        self.assertEqual(len(summary), 1)
        self.assertEqual(len(licenses), 1)
        self.assertEqual(len(base_includes), 1)
        self.assertEqual(image.count("IMAGE_INSTALL:append"), 1)
        self.assertNotRegex(image, r"(?i)(?:gguf|safetensors|llama-server|https?://|git://)")

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
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
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
            LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb",
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
        self.assertEqual(recipes[0].name, "readylinux-runtime_0.3.bb")
        self.assertEqual(recipes[1].name, "readylinux-console_0.1.bb")
        for recipe_path in recipes:
            recipe = recipe_path.read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"(?m)^LIC_FILES_CHKSUM\s*=", recipe)), 1, recipe_path.name)
            self.assertEqual(len(re.findall(r'(?m)^LICENSE\s*=\s*"MIT"$', recipe)), 1, recipe_path.name)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{32}", checksum) for checksum in checksums))

    def test_console_recipe_runtime_dependencies_include_every_required_package(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        dependency = re.search(r'RDEPENDS:\$\{PN\}\s*\+=\s*"([^"]+)"', recipe)
        self.assertIsNotNone(dependency)
        declared = set(dependency.group(1).split())

        inherited = re.search(r"(?m)^inherit\s+([^\n]+)$", recipe)
        self.assertIsNotNone(inherited)
        self.assertIn("systemd", inherited.group(1).split())
        self.assertTrue({"readylinux-runtime", "systemd"}.issubset(declared))
        self.assertEqual(declared, {"readylinux-runtime", "systemd"})

    def test_recipes_declare_license_provenance_and_runtime_dependencies(self):
        runtime = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        service = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        expected_license = 'LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"'
        for recipe in (runtime, service):
            self.assertIn('LICENSE = "MIT"', recipe)
            self.assertIn(expected_license, recipe)
            checksum_line = re.search(r"(?m)^LIC_FILES_CHKSUM = \"([^\"]+)\"$", recipe)
            self.assertIsNotNone(checksum_line)
            self.assertTrue(checksum_line.group(1).startswith("file://${COMMON_LICENSE_DIR}/MIT;md5="))
        self.assertIn('RDEPENDS:${PN} += "readylinux-runtime systemd"', service)
        self.assertIn("USERADD_PARAM:${PN}", service)
        self.assertIn('GROUPADD_PARAM:${PN} = "--system ready"', service)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', service)
        self.assertNotIn("AUTOREV", runtime + service)
        self.assertNotRegex(runtime + service, r"(?m)^\\s*(?:git|https?)://")

    def test_runtime_recipe_file_search_path_resolves_to_repository_root(self):
        recipe_path = LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb"
        recipe = recipe_path.read_text(encoding="utf-8")
        prepend = re.search(r'(?m)^FILESEXTRAPATHS:prepend\s*:?=\s*"([^"]+)"$', recipe)
        self.assertIsNotNone(prepend)
        expanded = prepend.group(1).replace("${THISDIR}", str(recipe_path.parent))
        search_path = (Path(expanded.rstrip(":")) / "readylinux.py").resolve()
        self.assertEqual(search_path.parent, ROOT.resolve())
        self.assertTrue(search_path.is_file())

    def test_runtime_recipe_is_allarch_and_declares_no_model_or_network_payload(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        self.assertRegex(recipe, r"(?m)^inherit\s+allarch\s*$")
        src_uri = re.search(r'(?m)^SRC_URI\s*=\s*"([^"]*)"', recipe)
        self.assertIsNotNone(src_uri)
        self.assertNotRegex(src_uri.group(1), r"(?i)(?:https?://|git://|\b(?:gguf|safetensors|llama-server)\b)")
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertIn(f"file://{source}", src_uri.group(1))
        self.assertIn('RDEPENDS:${PN} += "python3-core python3-difflib python3-crypt python3-json python3-misc python3-netclient python3-shell"', recipe)

    def test_runtime_recipe_launcher_matches_packaged_entrypoint_path(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        launcher = re.search(r"(?ms)^\s*cat > \$\{D\}\$\{bindir\}/readylinux <<'EOF'\n(.*?)\nEOF$", recipe)
        self.assertIsNotNone(launcher)
        exec_start = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        service_command = re.search(r"(?m)^ExecStart=(\S+)(?:\s|$)", exec_start)
        self.assertIsNotNone(service_command)
        self.assertEqual(service_command.group(1), "/usr/bin/readylinux")
        self.assertIn("exec python3 /usr/share/readylinux/readylinux.py \"$@\"", launcher.group(1))
        self.assertRegex(recipe, r"(?m)^\s*chmod 0755 \$\{D\}\$\{bindir\}/readylinux\s*$")
        self.assertIn('FILES:${PN} += "${datadir}/readylinux ${bindir}/readylinux"', recipe)

    def test_runtime_recipe_copies_each_declared_local_source_to_packaged_destination(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
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
        runtime = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        console = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        for installed_path in ("${datadir}/readylinux", "${bindir}/readylinux"):
            self.assertIn(installed_path, runtime)
            self.assertIn(installed_path, runtime.split("FILES:${PN} +=", 1)[1])
        for installed_path in ("${systemd_system_unitdir}/readylinux-console.service", "${sysconfdir}/systemd/system/getty@tty1.service"):
            self.assertIn(installed_path, console)
            self.assertIn(installed_path, console.split("FILES:${PN} +=", 1)[1])
        mask_destination = re.search(r"ln -s /dev/null \$\{D\}(\$\{sysconfdir\}/systemd/system/getty@tty1\.service)", console)
        self.assertIsNotNone(mask_destination)
        self.assertIn(mask_destination.group(1), console.split("FILES:${PN} +=", 1)[1])
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', console)
        self.assertEqual(len(re.findall(r"(?m)^\s*ln -s /dev/null \$\{D\}\$\{sysconfdir\}/systemd/system/getty@tty1\.service$", console)), 1)

    def test_recipe_dependencies_cover_non_core_stdlib_imports(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        dependency_match = re.search(r'RDEPENDS:\$\{PN\}\s*\+=\s*"([^"]+)"', recipe)
        self.assertIsNotNone(dependency_match, "RDEPENDS missing from runtime recipe")
        dependency_tokens = dependency_match.group(1).split()
        declared = set(dependency_tokens)
        self.assertEqual(len(dependency_tokens), len(declared), "duplicate runtime RDEPENDS package token")
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
        # The externally discovered llama-server executable is a runtime prerequisite too.
        required.add("python3-shell")
        self.assertTrue(required.issubset(declared), f"Missing RDEPENDS: {sorted(required - declared)}")
        self.assertEqual(declared, required, f"Unused RDEPENDS package entries: {sorted(declared - required)}")
        image = (LAYER / "recipes-core/images/readylinux-image.bb").read_text(encoding="utf-8")
        image_install = re.search(r'IMAGE_INSTALL:append\s*=\s*"([^"]+)"', image)
        self.assertIsNotNone(image_install)
        self.assertTrue({"readylinux-runtime", "readylinux-console"}.issubset(set(image_install.group(1).split())))

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
        self.assertEqual(useradd.group(1).split().count("--system"), 1)
        self.assertEqual(useradd.group(1).split().count("--no-create-home"), 1)
        self.assertIn("--shell /sbin/nologin", useradd.group(1))
        self.assertIn(f" {group}", groupadd.group(1))
        useradd_packages = re.search(r"(?m)^USERADD_PACKAGES\s*=\s*\"([^\"]+)\"$", recipe)
        self.assertIsNotNone(useradd_packages)
        useradd_scope = useradd_packages.group(1).split()
        self.assertEqual(useradd_scope, ["${PN}"])
        user_home = re.search(r"--home-dir\s+([^\s]+)", useradd.group(1))
        self.assertIsNotNone(user_home)
        state_directory = directives.get("StateDirectory", "")
        self.assertTrue(state_directory)
        self.assertIn(f"{state_directory}", directives.get("Environment", ""))
        self.assertEqual(directives.get("StateDirectoryMode"), "0750")
        self.assertEqual(user_home.group(1), "/var/lib/readylinux")
        self.assertEqual(directives.get("Environment"), "XDG_DATA_HOME=/var/lib/readylinux")
        self.assertEqual(directives.get("StateDirectory"), "readylinux")

        umask = directives.get("UMask")
        self.assertTrue(umask)
        umask_value = int(umask, 8)
        self.assertLessEqual(umask_value, 0o777)
        self.assertEqual(umask_value & 0o0750, 0, "UMask removes permissions required by the persistent state dir")
        self.assertIn(user_home.group(1), ("/var/lib/readylinux", directives.get("Environment", "")))

    def test_systemd_startup_order_and_exec_arguments_match_console_contract(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("After"), "local-fs.target")
        self.assertEqual(directives.get("ExecStart"), "/usr/bin/readylinux --workspace /var/lib/readylinux/programs")
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        workspace = re.search(r"--workspace\s+(\S+)", directives["ExecStart"])
        self.assertIsNotNone(workspace)
        self.assertEqual(workspace.group(1), "/var/lib/readylinux/programs")
        self.assertTrue(workspace.group(1).startswith("/var/lib/readylinux/"))

    def test_systemd_service_runs_with_explicit_restart_rate_limit(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("Restart"), "on-failure")
        self.assertRegex(directives.get("RestartSec", ""), r"^[1-9][0-9]*$")
        self.assertEqual(directives.get("Type"), "simple")

    def test_systemd_service_does_not_order_on_optional_network(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        unit_section = service.split("[Service]", 1)[0]
        self.assertIn("After=local-fs.target", unit_section)
        self.assertNotRegex(unit_section, r"(?im)^\s*(?:After|Wants|Requires)=.*(?:network|remote-fs)")
        self.assertIn("file://", (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8"))

    def test_systemd_service_declares_no_optional_unit_wants(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        dependency_lines = [line for line in service.splitlines() if re.match(r"^\s*(?:After|Before|Wants|Requires|BindsTo)=", line)]
        self.assertEqual(dependency_lines, ["After=local-fs.target"], "console should not acquire network/optional ordering")
        self.assertNotRegex("\\n".join(dependency_lines), r"(?i)(?:network|remote-fs|nfs)")

    def test_systemd_unit_descriptions_are_present_and_bounded(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        unit_match = re.search(r"(?m)^Description=(.+)$", service)
        self.assertIsNotNone(unit_match)
        description = unit_match.group(1)
        self.assertIn("READY Linux", description)
        self.assertLessEqual(len(description), 80, "service description should remain concise for boot/status output")
        self.assertFalse(any(ord(character) < 32 for character in description))

    def test_systemd_dependency_orders_critical_local_filesystem_before_console(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("After"), "local-fs.target")
        self.assertNotIn("network.target", directives.get("After", ""))
        self.assertNotIn("network-online.target", directives.get("After", ""))

    def test_systemd_console_reset_and_vhangup_tty_safety_are_enabled(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("TTYReset"), "yes")
        self.assertEqual(directives.get("TTYVHangup"), "yes")
        self.assertEqual(directives.get("TTYVTDisallocate"), "yes")
        self.assertEqual(directives.get("TTYPath"), "/dev/tty1")

    def test_systemd_console_requests_only_the_declared_device_tty(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("TTYPath"), "/dev/tty1")
        self.assertEqual(directives.get("StandardInput"), "tty")
        self.assertEqual(directives.get("StandardOutput"), "tty")
        self.assertNotIn("TTYPath=/dev/tty0", service)
        self.assertNotIn("TTYPath=/dev/console", service)
        self.assertEqual(len(re.findall(r"(?m)^TTYPath=", service)), 1)

    def test_systemd_console_tty_restart_and_logging_policy_are_explicit(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("StandardInput"), "tty")
        self.assertEqual(directives.get("StandardOutput"), "tty")
        self.assertEqual(directives.get("StandardError"), "journal")
        self.assertEqual(directives.get("TTYPath"), "/dev/tty1")
        self.assertEqual(directives.get("Restart"), "on-failure")
        self.assertRegex(directives.get("RestartSec", ""), r"^[1-9][0-9]*$")

    def test_systemd_unit_install_is_enabled_by_the_owning_recipe(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        unit_install = re.search(r"(?m)^WantedBy=([^\s]+)$", service)
        unit_name = re.search(r"(?m)^SYSTEMD_SERVICE:\$\{PN\}\s*=\s*\"([^\"]+)\"$", recipe)
        auto_enable = re.search(r"(?m)^SYSTEMD_AUTO_ENABLE:\$\{PN\}\s*=\s*\"([^\"]+)\"$", recipe)
        install_statement = re.search(r"(?m)^\s*install -m 0644 \$\{WORKDIR\}/([^\s]+) \$\{D\}\$\{systemd_system_unitdir\}/([^\s]+)$", recipe)
        self.assertIsNotNone(unit_install)
        self.assertIsNotNone(unit_name)
        self.assertIsNotNone(auto_enable)
        self.assertIsNotNone(install_statement)
        self.assertEqual(unit_name.group(1), "readylinux-console.service")
        self.assertEqual(auto_enable.group(1), "enable")
        self.assertEqual(install_statement.group(1), unit_name.group(1))
        self.assertEqual(install_statement.group(2), unit_name.group(1))
        self.assertIn("multi-user.target", unit_install.group(1))
        packaged_units = re.search(r'(?m)^FILES:\$\{PN\} \+= "([^"]+)"$', recipe)
        self.assertIsNotNone(packaged_units)
        self.assertIn("${systemd_system_unitdir}/readylinux-console.service", packaged_units.group(1))
        self.assertIn("${sysconfdir}/systemd/system/getty@tty1.service", packaged_units.group(1))

    def test_systemd_description_matches_console_identity_metadata(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        distro = (LAYER / "conf/distro/readylinux.conf").read_text(encoding="utf-8")
        description = re.search(r"(?m)^Description=(.+)$", service)
        distro_name = re.search(r'(?m)^DISTRO_NAME\s*=\s*"([^\"]+)"$', distro)
        self.assertIsNotNone(description)
        self.assertIsNotNone(distro_name)
        self.assertIn(distro_name.group(1), description.group(1))
        self.assertEqual(distro_name.group(1), "READY Linux")

    def test_systemd_startup_and_persistent_state_directives_match_service_type(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("Type"), "simple")
        self.assertEqual(directives.get("After"), "local-fs.target")
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        self.assertEqual(directives.get("StateDirectoryMode"), "0750")
        self.assertEqual(directives.get("UMask"), "0027")
        self.assertEqual(directives.get("ReadWritePaths"), "/var/lib/readylinux")

    def test_systemd_unit_has_required_sections_once_and_in_order(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        sections = [line.strip() for line in service.splitlines() if line.strip().startswith("[") and line.strip().endswith("]")]
        self.assertEqual(sections, ["[Unit]", "[Service]", "[Install]"])
        self.assertEqual(len(set(sections)), len(sections), "duplicate systemd section")
        self.assertEqual(service, service.rstrip() + "\n", "unit file should end with exactly one newline")
        self.assertFalse(any(line.rstrip() != line for line in service.splitlines()), "unit directives have trailing whitespace")

    def test_runtime_recipe_launcher_uses_posix_shell_and_exec_replacement(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        launcher = re.search(r"(?ms)^\s*cat > \$\{D\}\$\{bindir\}/readylinux <<'EOF'\n(.*?)\nEOF$", recipe)
        self.assertIsNotNone(launcher)
        lines = launcher.group(1).splitlines()
        self.assertEqual(lines[0], "#!/bin/sh")
        self.assertRegex(lines[1], r"^exec python3 /usr/share/readylinux/readylinux\.py \"\$@\"$")
        self.assertEqual(len(lines), 2, "launcher should not execute an intermediate shell command")

    def test_runtime_recipe_package_declares_expected_summary_and_description(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        summary = re.search(r'(?m)^SUMMARY\s*=\s*"([^"]+)"$', recipe)
        description = re.search(r'(?m)^DESCRIPTION\s*=\s*"([^"]+)"$', recipe)
        self.assertIsNotNone(summary)
        self.assertIsNotNone(description)
        self.assertIn("READY Linux", summary.group(1))
        self.assertIn("READY", description.group(1))
        self.assertNotIn("llama.cpp", summary.group(1))
        self.assertNotRegex(summary.group(1) + description.group(1), r"(?i)(?:https?://|git://|AUTOREV|gguf|safetensors)")
        self.assertEqual(len(re.findall(r"(?m)^SUMMARY\s*=", recipe)), 1)
        self.assertEqual(len(re.findall(r"(?m)^DESCRIPTION\s*=", recipe)), 1)

    def test_runtime_recipe_exposes_only_one_console_entrypoint_install(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        launcher_targets = re.findall(r"(?m)^\s*cat > \$\{D\}\$\{bindir\}/([^\s]+) <<'EOF'$", recipe)
        self.assertEqual(launcher_targets, ["readylinux"])
        chmod_targets = re.findall(r"(?m)^\s*chmod 0755 \$\{D\}\$\{bindir\}/([^\s]+)$", recipe)
        self.assertEqual(chmod_targets, launcher_targets)
        self.assertIn('FILES:${PN} += "${datadir}/readylinux ${bindir}/readylinux"', recipe)

    def test_runtime_recipe_stages_all_local_sources_before_launcher(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb").read_text(encoding="utf-8")
        install_block = recipe.split("do_install() {", 1)[1].split("\n}", 1)[0]
        source_copies = re.findall(
            r"(?m)^\s*install -m 0644 \$\{WORKDIR\}/([^\s]+) \$\{D\}\$\{datadir\}/readylinux/([^\s]+)$",
            install_block,
        )
        expected = {"readylinux.py", "basic.py", "ai_local.py", "vibe.py"}
        self.assertEqual({source for source, _dest in source_copies}, expected)
        self.assertEqual({dest for _source, dest in source_copies}, expected)
        self.assertEqual(source_copies, [(name, name) for name in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py")])

    def test_console_recipe_scopes_user_and_system_group_creation_to_package(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^USERADD_PACKAGES\s*=", recipe)), 1)
        self.assertEqual(len(re.findall(r"(?m)^USERADD_PARAM:\$\{PN\}\s*=", recipe)), 1)
        self.assertEqual(len(re.findall(r"(?m)^GROUPADD_PARAM:\$\{PN\}\s*=", recipe)), 1)
        self.assertEqual(len(re.findall(r"(?m)^GROUPADD_PARAM(?:_[A-Za-z]|:append|:prepend|:remove)", recipe)), 0)

    def test_console_recipe_has_unique_package_scoped_systemd_settings(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        for variable in ("SYSTEMD_SERVICE", "SYSTEMD_AUTO_ENABLE"):
            pattern = rf"(?m)^{variable}:\$\{{PN\}}\s*="
            self.assertEqual(len(re.findall(pattern, recipe)), 1, f"expected exactly one {variable}:${{PN}} setting")
        self.assertIn('SYSTEMD_SERVICE:${PN} = "readylinux-console.service"', recipe)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', recipe)

    def test_console_recipe_package_paths_do_not_use_legacy_override_syntax(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        modern_variables = r"(?:SYSTEMD_SERVICE|SYSTEMD_AUTO_ENABLE|RDEPENDS|FILES|USERADD_PARAM|GROUPADD_PARAM)"
        self.assertNotRegex(recipe, rf"(?m)^\s*{modern_variables}_[A-Za-z]\w*\s*[+:?]?=")
        self.assertNotRegex(recipe, rf"(?m)^\s*{modern_variables}:(?:append|prepend|remove)\s*=")
        self.assertRegex(recipe, r"(?m)^SYSTEMD_SERVICE:\$\{PN\}\s*=")
        self.assertRegex(recipe, r"(?m)^SYSTEMD_AUTO_ENABLE:\$\{PN\}\s*=")
        self.assertRegex(recipe, r"(?m)^RDEPENDS:\$\{PN\}\s*\+=")
        for variable in ("SYSTEMD_SERVICE", "SYSTEMD_AUTO_ENABLE", "RDEPENDS"):
            self.assertEqual(len(re.findall(rf"(?m)^{variable}:\$\{{PN\}}", recipe)), 1, f"duplicate {variable}:${{PN}} override")

    def test_console_recipe_useradd_contract_is_scoped_and_noninteractive(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        package_scope = re.search(r"(?m)^USERADD_PACKAGES\s*=\s*\"([^\"]+)\"$", recipe)
        useradd = re.search(r"(?m)^USERADD_PARAM:\$\{PN\}\s*=\s*\"([^\"]+)\"$", recipe)
        groupadd = re.search(r"(?m)^GROUPADD_PARAM:\$\{PN\}\s*=\s*\"([^\"]+)\"$", recipe)
        self.assertIsNotNone(package_scope)
        self.assertIsNotNone(useradd)
        self.assertIsNotNone(groupadd)
        self.assertEqual(package_scope.group(1).split(), ["${PN}"])
        self.assertIn("--system", useradd.group(1).split())
        self.assertIn("--no-create-home", useradd.group(1).split())
        self.assertIn("--shell /sbin/nologin", useradd.group(1))
        self.assertEqual(groupadd.group(1), "--system ready")
        self.assertEqual(recipe.count("--shell /sbin/nologin"), 1)
        self.assertEqual(recipe.count("--home-dir /var/lib/readylinux"), 1)

    def test_systemd_install_target_has_one_entry_and_recipe_enablement_matches(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        wanted_by = re.findall(r"(?m)^WantedBy=([^\s]+)$", service)
        enabled_units = re.findall(r'(?m)^SYSTEMD_SERVICE:\$\{PN\}\s*=\s*"([^"]+)"$', recipe)
        self.assertEqual(wanted_by, ["multi-user.target"])
        self.assertEqual(enabled_units, ["readylinux-console.service"])
        self.assertEqual(len(re.findall(r"(?m)^WantedBy=", service)), 1)
        self.assertEqual(re.findall(r"(?m)^WantedBy=([^\s]+)$", service), ["multi-user.target"])
        self.assertEqual(service.count("[Install]"), 1)
        self.assertIn('SYSTEMD_AUTO_ENABLE:${PN} = "enable"', recipe)
        self.assertIn('FILES:${PN} += "${systemd_system_unitdir}/readylinux-console.service ${sysconfdir}/systemd/system/getty@tty1.service"', recipe)
        self.assertEqual(len(re.findall(r"(?m)^SYSTEMD_SERVICE:\$\{PN\}", recipe)), 1)
        self.assertEqual(len(re.findall(r"(?m)^SYSTEMD_AUTO_ENABLE:\$\{PN\}", recipe)), 1)

    def test_systemd_unit_has_single_install_target_declaration(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        install_section = service.split("[Install]", 1)
        self.assertEqual(len(install_section), 2, "unit must declare one install section")
        before_install, install_body = install_section
        self.assertNotIn("[Install]", install_body, "unit must not repeat install section")
        wanted_by = re.findall(r"(?m)^WantedBy=([^\s]+)$", install_body)
        self.assertEqual(wanted_by, ["multi-user.target"])
        self.assertNotRegex(before_install, r"(?m)^WantedBy=")

    def test_console_package_file_list_has_no_duplicate_entries(self):
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        files_assignment = re.search(r'(?m)^FILES:\$\{PN\} \+= "([^"]+)"$', recipe)
        self.assertIsNotNone(files_assignment)
        paths = files_assignment.group(1).split()
        self.assertEqual(len(paths), len(set(paths)), "duplicate packaged console path")
        self.assertEqual(set(paths), {
            "${systemd_system_unitdir}/readylinux-console.service",
            "${sysconfdir}/systemd/system/getty@tty1.service",
        })

    def test_systemd_console_has_only_one_definition_per_directive(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = [line.split("=", 1)[0] for line in service.splitlines() if "=" in line and not line.startswith("#")]
        self.assertEqual(len(directives), len(set(directives)), "duplicate unit directives can override the intended policy")
        self.assertIn("User", directives)
        self.assertIn("ExecStart", directives)
        self.assertIn("ReadWritePaths", directives)

    def test_systemd_console_runs_without_privilege_escalation_or_writable_system_paths(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        directives = {
            line.split("=", 1)[0]: line.split("=", 1)[1]
            for line in service.splitlines()
            if "=" in line and not line.startswith("#")
        }
        self.assertEqual(directives.get("User"), "ready")
        self.assertEqual(directives.get("Group"), "ready")
        self.assertEqual(directives.get("NoNewPrivileges"), "yes")
        self.assertEqual(directives.get("ProtectSystem"), "strict")
        self.assertEqual(directives.get("ProtectHome"), "yes")
        self.assertEqual(directives.get("PrivateTmp"), "yes")
        self.assertEqual(directives.get("ProtectClock"), "yes")
        self.assertEqual(directives.get("ProtectKernelLogs"), "yes")
        self.assertEqual(directives.get("ProtectControlGroups"), "yes")
        self.assertEqual(directives.get("ProtectKernelModules"), "yes")
        self.assertEqual(directives.get("ProtectKernelTunables"), "yes")
        self.assertEqual(directives.get("ProtectHostname"), "yes")
        self.assertEqual(directives.get("RestrictSUIDSGID"), "yes")
        self.assertEqual(directives.get("LockPersonality"), "yes")
        self.assertEqual(directives.get("RemoveIPC"), "yes")
        self.assertEqual(directives.get("ReadWritePaths"), "/var/lib/readylinux")
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        for system_path in ("/etc", "/usr", "/opt", "/home"):
            self.assertNotIn(system_path, directives.get("ReadWritePaths", ""))

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
        writable_path = Path(directives["ReadWritePaths"])
        state_root = Path("/var/lib") / directives["StateDirectory"]
        self.assertEqual(writable_path, state_root)
        self.assertEqual(directives.get("StateDirectory"), "readylinux")
        self.assertEqual(directives.get("StateDirectoryMode"), "0750")
        self.assertEqual(int(directives["StateDirectoryMode"], 8), 0o750)
        self.assertEqual(len(re.findall(r"(?m)^StateDirectory=", service)), 1)
        self.assertEqual(len(re.findall(r"(?m)^StateDirectoryMode=", service)), 1)
        self.assertEqual(directives.get("UMask"), "0027")
        self.assertLessEqual(int(directives["UMask"], 8), 0o027)
        umask = int(directives["UMask"], 8)
        directory_mode = int(directives["StateDirectoryMode"], 8)
        self.assertEqual(umask & directory_mode, 0)
        self.assertEqual(directives.get("Environment"), "XDG_DATA_HOME=/var/lib/readylinux")
        self.assertEqual(len(re.findall(r"(?m)^Environment=", service)), 1)
        self.assertEqual(directives.get("Type"), "simple")
        self.assertEqual(directives.get("StandardInput"), "tty")
        self.assertEqual(directives.get("StandardOutput"), "tty")
        self.assertEqual(directives.get("TTYPath"), "/dev/tty1")
        self.assertEqual(directives.get("Restart"), "on-failure")
        self.assertEqual(directives.get("RestartSec"), "1")
        useradd = re.search(r'USERADD_PARAM:\$\{PN\}\s*=\s*"([^"]+)"', recipe)
        self.assertIsNotNone(useradd)
        self.assertIn("--home-dir /var/lib/readylinux", useradd.group(1))
        self.assertIn("--gid ready", useradd.group(1))
        workspace = re.search(r"--workspace\s+(\S+)", directives["ExecStart"])
        self.assertIsNotNone(workspace)
        home_path = useradd.group(1).split("--home-dir ", 1)[1].split()[0]
        self.assertEqual(PurePosixPath(home_path) / "programs", PurePosixPath(workspace.group(1)))
        self.assertIn("/var/lib/readylinux/programs", workspace.group(1))
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
        self.assertIn('RDEPENDS:${PN} += "readylinux-runtime systemd"', recipe)
        for docs in (italian, english):
            self.assertIn("readylinux-console", docs)
            self.assertIn("getty@tty1.service", docs)
            self.assertIn("ready", docs)
            self.assertIn('readylinux-console` declares `RDEPENDS:${PN} += "readylinux-runtime systemd"`', docs)
            self.assertIn("`FILES:${PN}`", docs)
            self.assertIn("readylinux-console.service", docs)
        self.assertIn('FILES:${PN} += "${systemd_system_unitdir}/readylinux-console.service ${sysconfdir}/systemd/system/getty@tty1.service"', recipe)

    def test_layer_docs_make_distro_machine_and_cached_sources_requirements_explicit(self):
        for doc_path in (LAYER / "README.md", LAYER / "README.en.md"):
            doc = doc_path.read_text(encoding="utf-8")
            self.assertIn('DISTRO = "readylinux"', doc)
            self.assertIn('MACHINE = "<selected-bsp-machine>"', doc)
            self.assertIn("release series", doc.lower())
            self.assertTrue("cached" in doc.lower() or "cache" in doc.lower())
            self.assertLess(doc.index("DISTRO ="), doc.index("bash scripts/validate-yocto-env.sh"))

    @staticmethod
    def _fenced_command_lines(text):
        commands = []
        in_block = False
        for line in text.splitlines():
            if line.startswith("```"):
                in_block = not in_block
                continue
            if not in_block:
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            commands.append(stripped)
        return commands

    def test_layer_readme_command_blocks_match_between_languages(self):
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        self.assertEqual(self._fenced_command_lines(italian), self._fenced_command_lines(english))
        script_pattern = r"scripts/[A-Za-z0-9_.-]+\.(?:sh|py)"
        self.assertEqual(set(re.findall(script_pattern, italian)), set(re.findall(script_pattern, english)))
        for script in set(re.findall(script_pattern, italian)):
            with self.subTest(script=script):
                self.assertTrue((ROOT / script).is_file(), f"documented script missing: {script}")

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
        self.assertNotIn("$data", json.dumps(schema), "schema must not depend on extension keywords to express shape")
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
        self.assertEqual(example["identity"]["host_arch"], "UNRECORDED")
        self.assertEqual(example["identity"]["machine"], "UNSELECTED")
        self.assertEqual(example["identity"]["distro"], "readylinux")
        self.assertEqual(example["identity"]["tclibc"], "")
        self.assertEqual(example["identity"]["bsp_revision"], "")
        self.assertEqual(example["identity"]["init_system"], "systemd")
        self.assertEqual(example["identity"]["bitbake_version"], "NOT-RUN")
        self.assertEqual(example["identity"]["poky_commit"], "0" * 40)
        self.assertEqual(example["identity"]["readylinux_commit"], "0" * 40)
        self.assertEqual(example["identity"]["layer_commits"], [])
        self.assertEqual(example["identity"]["tclibc"], "")
        self.assertEqual(example["identity"]["utc_date"], "2000-01-01T00:00:00Z")
        self.assertRegex(example["identity"]["utc_date"], r"^2000-01-01T00:00:00Z$")
        self.assertEqual(example["environment"]["bblayers_conf_sha256"], "0" * 64)
        self.assertEqual(example["environment"]["local_conf_sha256"], "0" * 64)
        self.assertIsNone(example["image"]["artifact_path"])
        self.assertIsNone(example["image"]["artifact_format"])
        self.assertIsNone(example["image"]["artifact_size_bytes"])
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
        self.assertIsNone(example["environment"]["parse_exit_code"])
        self.assertEqual(example["environment"]["parse_log"], "NOT-RUN")
        self.assertEqual(example["image"]["source_cache_state"], "not-built")
        self.assertIsNone(example["image"]["exit_code"])
        self.assertIsNone(example["image"]["build_log"])
        self.assertIsNone(example["image"]["artifact_path"])
        self.assertIsNone(example["image"]["artifact_format"])
        self.assertIsNone(example["image"]["artifact_size_bytes"])
        self.assertIsNone(example["image"]["sha256"])
        self.assertEqual(example["boot"]["status"], "not-run")
        self.assertIsNone(example["boot"]["qemu_version"])
        self.assertIsNone(example["boot"]["command"])
        self.assertIsNone(example["boot"]["console_log"])
        for field in ("ready_console", "unprivileged_service", "persistent_state", "getty_mask", "basic_smoke", "offline_smoke"):
            self.assertEqual(example["boot"][field], "not-run")
        self.assertEqual(example["verdict"], "not-verified")
        if example["image"]["source_cache_state"] == "not-built":
            self.assertIsNone(example["image"]["exit_code"])
            self.assertIsNone(example["image"]["build_log"])
            self.assertIsNone(example["image"]["artifact_path"])
            self.assertIsNone(example["image"]["artifact_format"])
            self.assertIsNone(example["image"]["artifact_size_bytes"])
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

    def test_build_evidence_records_the_oe_release_series(self):
        schema = json.loads((ROOT / "docs/YOCTO_BUILD_EVIDENCE.schema.json").read_text(encoding="utf-8"))
        example = json.loads((ROOT / "docs/YOCTO_BUILD_EVIDENCE.example.json").read_text(encoding="utf-8"))
        self.assertIn("oe_series", schema["properties"]["identity"]["required"])
        self.assertEqual(example["identity"]["oe_series"], "UNVERIFIED")
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        match = re.search(r"(?m)^LAYERSERIES_COMPAT_readylinux = \"([^\"]+)\"$", layer_conf)
        self.assertIsNotNone(match)
        for name in ("YOCTO_BUILD_EVIDENCE_TEMPLATE.md", "YOCTO_BUILD_EVIDENCE_TEMPLATE.en.md"):
            template = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn("OE release series", template, name)
            self.assertIn("LAYERSERIES_COMPAT_core", template, name)

    def test_build_evidence_example_marks_every_execution_stage_unverified(self):
        schema = json.loads((ROOT / "docs/YOCTO_BUILD_EVIDENCE.schema.json").read_text(encoding="utf-8"))
        example = json.loads((ROOT / "docs/YOCTO_BUILD_EVIDENCE.example.json").read_text(encoding="utf-8"))
        self.assertEqual(example["environment"]["parse_exit_code"], None)
        self.assertEqual(example["environment"]["parse_log"], "NOT-RUN")
        self.assertEqual(example["identity"]["bitbake_version"], "NOT-RUN")
        self.assertEqual(example["image"]["build_command"], "NOT-RUN")
        self.assertEqual(example["image"]["source_cache_state"], "not-built")
        self.assertIsNone(example["image"]["exit_code"])
        self.assertIsNone(example["image"]["artifact_path"])
        self.assertIsNone(example["image"]["sha256"])
        self.assertEqual(example["boot"]["status"], "not-run")
        self.assertEqual(example["verdict"], "not-verified")
        allowed_verdicts = schema["properties"]["verdict"]["enum"]
        self.assertIn(example["verdict"], allowed_verdicts)
        self.assertNotEqual(example["verdict"], "reproducible-and-booted")

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

    def test_layer_recipe_file_sources_resolve_for_runtime_recipe_and_console_recipe(self):
        runtime_recipe = LAYER / "recipes-ready/readylinux/readylinux-runtime_0.3.bb"
        console_recipe = LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb"

        runtime_sources = (runtime_recipe.parent / "../../../").resolve()
        console_sources = (console_recipe.parent / "..").resolve()

        self.assertEqual(runtime_sources, ROOT.resolve())
        self.assertEqual(console_sources, (LAYER / "recipes-core").resolve())
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertTrue((runtime_sources / source).is_file(), source)
        console_file_search_roots = (console_sources / "readylinux", console_sources)
        self.assertTrue(any((base / "readylinux-console.service").is_file() for base in console_file_search_roots))

    def test_host_preflight_evidence_has_current_independent_wsl_gate_result(self):
        italian = (ROOT / "docs/TEST_RESULTS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/TEST_RESULTS.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            with self.subTest(report="Italian" if doc == italian else "English"):
                self.assertIn("19/19", doc)
                self.assertIn("INCOMPLETE", doc)
                self.assertIn("BUILDDIR", doc)
                self.assertIn("bitbake-layers", doc)
                self.assertTrue("read-only" in doc.lower() or "sola lettura" in doc.lower())
                self.assertRegex(doc, r"(?i)(?:exit 1.*INCOMPLETE|INCOMPLETE.*exit 1)")

    def test_layer_docs_define_reproducibility_evidence(self):
        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        for requirement in ("Poky/OE-Core commit", "MACHINE", "bitbake -p", "checksums", "QEMU"):
            self.assertIn(requirement, italian)
            self.assertIn(requirement, english)

    def test_test_results_has_current_firing_snapshot_and_command_evidence(self):
        italian = (ROOT / "docs/TEST_RESULTS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/TEST_RESULTS.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            with self.subTest(report="Italian" if doc == italian else "English"):
                self.assertIn("compileall", doc)
                self.assertIn("unittest discover -s tests -v", doc)
                self.assertIn("bash -n", doc)
                self.assertIn("QEMU", doc)
                self.assertIn("bash scripts/check-yocto-host.sh", doc)
                self.assertRegex(doc, r"(?m)^- (?:Comandi|Commands):")
                self.assertTrue(("preflight" in doc.lower() or "probe" in doc.lower()) and "INCOMPLETE" in doc)
                self.assertRegex(doc, r"full suite:?\s+\d+ tests PASS")
                self.assertRegex(doc, r"(?i)(?:\d+ platform-specific skips|\d+ skip platform-specific)")
                snapshot = re.search(
                    r"(?m)^- (?:Snapshot iniziale (?:confermato via|verificato con)|Initial snapshot verified by) `git rev-parse HEAD`: `([0-9a-f]{40})`",
                    doc,
                )
                self.assertIsNotNone(snapshot, f"missing firing-start HEAD snapshot in {'Italian' if doc == italian else 'English'} results")
                self.assertIn("git status --short --branch", doc)

        statuses = (
            (ROOT / "docs/STATUS.md").read_text(encoding="utf-8"),
            (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8"),
        )
        reported_heads = []
        for status in statuses:
            match = re.search(r"(?m)^- \*\*Git\*\*: firing-start HEAD `([0-9a-f]{40})`", status)
            self.assertIsNotNone(match, "status must record firing-start HEAD")
            reported_heads.append(match.group(1))
        self.assertEqual(len(set(reported_heads)), 1, "Italian and English status firing HEADs diverge")

    def test_layer_release_series_claims_are_documented_as_unverified_bilingually(self):
        layer_conf = (LAYER / "conf/layer.conf").read_text(encoding="utf-8")
        compatibility = re.search(r"(?m)^LAYERSERIES_COMPAT_readylinux = \"([^\"]+)\"$", layer_conf)
        self.assertIsNotNone(compatibility)
        supported_series = compatibility.group(1).split()
        self.assertTrue(supported_series)
        self.assertEqual(len(supported_series), len(set(supported_series)))

        italian = (LAYER / "README.md").read_text(encoding="utf-8")
        english = (LAYER / "README.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            with self.subTest(doc="Italian" if doc == italian else "English"):
                for series in supported_series:
                    self.assertIn(series, doc)
                self.assertRegex(doc.lower(), r"(?:has|have) not yet been verified")
                self.assertIn("scarthgap is verified", doc)
                self.assertIn("104772c5fd0653290cbb5e4b77813343957939cc", doc)

    def test_layer_service_preserves_state_directory_for_service_user(self):
        service = (LAYER / "recipes-core/readylinux/readylinux-console.service").read_text(encoding="utf-8")
        recipe = (LAYER / "recipes-core/readylinux/readylinux-console_0.1.bb").read_text(encoding="utf-8")
        self.assertIn("StateDirectory=readylinux", service)
        self.assertIn("StateDirectoryMode=0750", service)
        self.assertIn("UMask=0027", service)
        self.assertIn('GROUPADD_PARAM:${PN} = "--system ready"', recipe)
        self.assertRegex(recipe, r"(?m)^USERADD_PARAM:\$\{PN\}.*--system --gid ready --home-dir /var/lib/readylinux")
        self.assertIn("NoNewPrivileges=yes", service)
        self.assertIn("ProtectSystem=strict", service)

    def test_status_records_current_test_baseline_and_bitbake_limitation(self):
        italian = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        for doc in (italian, english):
            self.assertIn("249", doc)
            self.assertIn("**Verificato localmente**" if "Stato READY" in doc else "**Locally verified**", doc)
            self.assertTrue("qemu" in doc.lower() or "hardware" in doc.lower() or "BUILDDIR" in doc or "FIFO" in doc or "IMAGE_INSTALL" in doc or "recipe" in doc.lower() or "file://" in doc or "validator" in doc.lower())
            self.assertIn("BitBake", doc)
            self.assertIn("QEMU", doc)
            self.assertIn(".pi-loop.json", doc)
            self.assertTrue("HEAD" in doc or "firing-start" in doc.lower())
            self.assertRegex(doc, r"(?m)- \*\*Git\*\*: firing-start HEAD `[0-9a-f]{40}`")

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

    def test_roadmap_m1_claims_match_console_and_basic_reality(self):
        console = (ROOT / "readylinux.py").read_text(encoding="utf-8")
        self.assertIn("BasicProgram", console)
        self.assertIn("SAVE", console)
        self.assertIn("LOAD", console)
        for doc in ("docs/BASIC.md", "docs/BASIC.en.md"):
            self.assertTrue((ROOT / doc).is_file(), doc)
        italian = (ROOT / "docs/ROADMAP.md").read_text(encoding="utf-8").lower()
        english = (ROOT / "docs/ROADMAP.en.md").read_text(encoding="utf-8").lower()
        for text, language in ((italian, "it"), (english, "en")):
            with self.subTest(language=language):
                self.assertNotIn("remain incomplete", text)
                self.assertRegex(text, r"not (?:claimed|dichiarata)|non dichiarata")

    def test_roadmap_states_parse_verified_and_build_unverified(self):
        for path in (ROOT / "docs/ROADMAP.md", ROOT / "docs/ROADMAP.en.md"):
            with self.subTest(doc=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("104772c5fd0653290cbb5e4b77813343957939cc", text)
                self.assertRegex(text, r"0 (?:errors|errori)")
                self.assertRegex(text.lower(), r"unverified|non verificat")
                self.assertNotIn("19/19", text, "the stale 19-command tally must not come back")
                self.assertIn("wic", text)

    def test_verification_plan_records_the_pinned_parse_evidence(self):
        plan = (ROOT / "docs/VERIFICATION_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("104772c5fd0653290cbb5e4b77813343957939cc", plan)
        self.assertIn("0 errors", plan)
        self.assertIn("usrmerge", plan)
        self.assertIn("readylinux-runtime", plan)
        self.assertIn("24", plan, "the plan must state the current host-command count")
        self.assertIn("lz4c", plan)
        self.assertIn("bitbake -n readylinux-image", plan)

    def test_status_docs_record_the_wsl_debian_probe_result_not_a_windows_shell_run(self):
        for doc_path in (ROOT / "docs/STATUS.md", ROOT / "docs/STATUS.en.md"):
            doc = doc_path.read_text(encoding="utf-8")
            with self.subTest(doc=doc_path.name):
                self.assertIn("19/19", doc, "status must record the WSL Debian preflight command tally")
                self.assertIn("WSL Debian 13", doc)
                self.assertIn("bitbake", doc.lower())
                self.assertNotRegex(doc, r"(?i)comandi host[^\n]{0,40}mancanti")
                self.assertNotRegex(doc, r"(?i)host commands[^\n]{0,40}missing")
                self.assertRegex(doc, r"(?i)(?:shell Windows|Windows shell)")
                self.assertIn("BUILDDIR", doc)
                self.assertRegex(doc, r"(?i)19/19[^\n]{0,200}(?:OK|present|trovat)")
                self.assertNotRegex(
                    doc,
                    r"(?i)(?:10|11)\s+(?:host commands|comandi host)\s+(?:missing|mancanti)",
                    "Windows-shell probe output must not be recorded as Debian host evidence",
                )

    def test_status_docs_state_current_build_limits_and_host_prereqs(self):
        italian = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        english = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        cases = (
            (italian, "Non verificato", r"(?m)^- \*\*Verificato localmente\*\*", "249 test Windows/Python 3.11"),
            (english, "Not verified", r"(?m)^- \*\*Locally verified\*\*", "249 Windows/Python 3.11 tests"),
        )
        for doc, localized_status, baseline_heading, expected_count in cases:
            self.assertIn("BitBake", doc)
            self.assertIn("QEMU", doc)
            self.assertIn(localized_status, doc)
            self.assertRegex(doc, baseline_heading)
            self.assertIn(expected_count, doc)
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
        security_it = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        security_en = (ROOT / "docs/STATUS.en.md").read_text(encoding="utf-8")
        for doc in (security_it, security_en):
            self.assertIn("--security", doc)
            self.assertIn("8.0", doc)
            self.assertIn("exit 7", doc)

    def test_layer_documentation_warns_build_not_verified(self):
        readme = (LAYER / "README.md").read_text(encoding="utf-8")
        self.assertIn("BitBake and QEMU unavailable", readme)
        self.assertIn("does not clone repositories or download source", readme)
        self.assertIn("does not provide a normal login prompt there", readme)


if __name__ == "__main__":
    unittest.main()
