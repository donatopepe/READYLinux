import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/YOCTO_PREFLIGHT_RECORD.schema.json"
EXAMPLE = ROOT / "docs/YOCTO_PREFLIGHT_RECORD.example.json"
RECORDER = ROOT / "scripts/record-yocto-preflight.py"
REQUIRED_COMMANDS = (
    "bash", "git", "gcc", "g++", "make", "python3", "chrpath", "cpio",
    "diffstat", "file", "gawk", "ip", "ping", "socat", "texi2any", "unzip",
    "wget", "xz", "zstd", "uname", "getconf",
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_matches_schema(test, record, schema):
    test.assertEqual(set(record), set(schema["required"]))
    test.assertRegex(record["recorded_utc"], schema["properties"]["recorded_utc"]["pattern"])
    test.assertRegex(record["readylinux_commit"], schema["properties"]["readylinux_commit"]["pattern"])
    test.assertEqual(record["schema_version"], 1)
    preflight = record["preflight"]
    preflight_schema = schema["properties"]["preflight"]
    test.assertEqual(set(preflight), set(preflight_schema["required"]))
    test.assertEqual(set(preflight["os"]), {"name", "id"})
    test.assertIsInstance(preflight["cpus"], int)
    test.assertGreaterEqual(preflight["cpus"], 0)
    test.assertIn(preflight["verdict"], preflight_schema["properties"]["verdict"]["enum"])
    for name, found in preflight["required"].items():
        test.assertIsInstance(name, str)
        test.assertIsInstance(found, bool)
    for name, found in preflight["optional"].items():
        test.assertIsInstance(name, str)
        test.assertIsInstance(found, bool)
    for name in preflight["missing_required"]:
        test.assertIsInstance(name, str)
        test.assertTrue(name)
    test.assertEqual(set(preflight["builddir"]), {"set", "path"})
    test.assertIsInstance(preflight["builddir"]["set"], bool)


class PreflightRecordSchemaTests(unittest.TestCase):
    def test_schema_is_standard_json_schema_without_prose_escape_hatches(self):
        schema = load(SCHEMA)
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertNotIn("$data", json.dumps(schema))
        self.assertEqual(set(schema["properties"]["preflight"]["properties"]["verdict"]["enum"]),
                         {"ready", "incomplete", "not-a-linux-host"})
        self.assertEqual(schema["properties"]["schema_version"]["const"], 1)

    def test_example_is_placeholder_only_and_structurally_valid(self):
        schema = load(SCHEMA)
        example = load(EXAMPLE)
        assert_matches_schema(self, example, schema)
        self.assertEqual(example["readylinux_commit"], "0" * 40)
        self.assertEqual(example["recorded_utc"], "2000-01-01T00:00:00Z")
        self.assertIn("not build evidence", example["scope"])
        self.assertTrue(example["preflight"]["os"]["name"].startswith("EXAMPLE"))

    def test_example_ready_verdict_requires_builddir_and_bitbake(self):
        example = load(EXAMPLE)
        preflight = example["preflight"]
        if preflight["verdict"] == "ready":
            self.assertTrue(preflight["builddir"]["set"])
            self.assertTrue(preflight["optional"]["bitbake"])
            self.assertTrue(preflight["optional"]["bitbake-layers"])
            self.assertEqual(preflight["missing_required"], [])

    @unittest.skipIf(os.name == "nt", "PATH executable stubs require Unix")
    def test_recorder_output_matches_schema(self):
        schema = load(SCHEMA)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fakebin = root / "bin"
            fakebin.mkdir()
            for name in REQUIRED_COMMANDS + ("bitbake", "bitbake-layers"):
                stub = fakebin / name
                stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                stub.chmod(0o755)
            builddir = root / "build"
            builddir.mkdir()
            os_release = root / "os-release"
            os_release.write_text('PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\n', encoding="utf-8")
            output = root / "record.json"
            bash = subprocess.check_output(["bash", "-lc", "command -v bash"], text=True).strip()
            git = subprocess.check_output(["bash", "-lc", "command -v git"], text=True).strip()
            result = subprocess.run(
                [sys.executable, str(RECORDER), str(output), "--repo", str(ROOT)],
                cwd=ROOT,
                env={
                    "PATH": str(fakebin),
                    "BUILDDIR": str(builddir),
                    "READYLINUX_OS_RELEASE": str(os_release),
                    "READYLINUX_BASH": bash,
                    "READYLINUX_GIT": git,
                },
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = load(output)
        assert_matches_schema(self, record, schema)
        self.assertEqual(record["preflight"]["verdict"], "ready")
        self.assertIn("not build evidence", record["scope"])


if __name__ == "__main__":
    unittest.main()
