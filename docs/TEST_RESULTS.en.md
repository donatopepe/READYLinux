# Test Results

## 2026-10-18 — Evidence-template secret warning

- IT/EN templates explicitly warn to redact secrets and not attach credentials in config checksum evidence.
- Focused `python -m unittest tests.test_yocto_scaffold.YoctoScaffoldTests.test_build_evidence_templates_include_required_provenance_and_results -v` — PASS.
- Full suite `python -m unittest discover -s tests -v` — PASS, 57 tests; compileall, `bash -n`, `git diff --check` — PASS.
- No real build/data inserted.
