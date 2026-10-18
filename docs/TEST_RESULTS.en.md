# Test Results

## 2026-10-18 — JSON schema example safety

- Strengthened stdlib checks for commit/checksum patterns, enums, nullable exit/artifact fields, not-built/not-boot states.
- JSON is placeholder sample, not build evidence; schema comment warns zero hashes/NOT-RUN markers are not evidence.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
