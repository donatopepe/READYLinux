# Test Results

## 2026-10-18 — Machine-readable Yocto evidence schema

- Added `docs/YOCTO_BUILD_EVIDENCE.schema.json`, Draft 2020-12, no additional Python dependencies.
- `json.loads` and required sections/audit fields test — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
- No build evidence/results fabricated.
