# Test Results

## 2026-10-18 — Not-run evidence invariants

- JSON sample checks: not-built implies null exit/artifact/checksum; not-run boot implies all smoke checks are not-run.
- Focused `test_build_evidence_schema_is_valid_json_with_audit_fields` — PASS.
- Full suite `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
