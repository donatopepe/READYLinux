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
        self.assertIn('IMAGE_INSTALL:append = " readylinux"', image)

    def test_recipe_includes_runtime_sources_and_no_external_fetch(self):
        recipe = (LAYER / "recipes-ready/readylinux/readylinux_0.3.bb").read_text(encoding="utf-8")
        for source in ("readylinux.py", "basic.py", "ai_local.py", "vibe.py"):
            self.assertIn(f"file://{source}", recipe)
        self.assertNotRegex(recipe, r"(?m)^\s*(?:git|https?)://")
        self.assertIn('LICENSE = "MIT"', recipe)
        self.assertIn("exec python3", recipe)

    def test_layer_documentation_warns_build_not_verified(self):
        readme = (LAYER / "README.md").read_text(encoding="utf-8")
        self.assertIn("BitBake and QEMU unavailable", readme)
        self.assertIn("does not clone repositories or download source", readme)


if __name__ == "__main__":
    unittest.main()
