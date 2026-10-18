# Test Results

## 2026-10-18 — Evidence schema negative cases

- Placeholder JSON example checked against required fields, nested shape, commit/hash patterns, and enums.
- Added negative assertions for malformed commit, invalid verdict, and missing required field.
- Focused `test_build_evidence_schema_is_valid_json_with_audit_fields` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS. No external JSON Schema library used.
