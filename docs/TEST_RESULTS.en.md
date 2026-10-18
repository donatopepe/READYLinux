# Test Results

## 2026-10-18 — Evidence example record

- Added `docs/YOCTO_BUILD_EVIDENCE.example.json`, explicitly not-built/not-verified record.
- Draft 2020-12 schema now requires `deviations`; test checks top-level key alignment and not-run states.
- Schema/example test — PASS; suite `python -m unittest discover -s tests -v` — PASS, 58 tests.
- compileall, `bash -n`, `git diff --check` — PASS.
