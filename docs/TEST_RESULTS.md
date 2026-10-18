# Risultati test

## 2026-10-18 — Invarianti record non eseguito

- Esempio JSON testato: not-built → nessun exit/artifact/checksum; not-run boot → tutti gli smoke check not-run.
- Test mirato `test_build_evidence_schema_is_valid_json_with_audit_fields` — PASS.
- Suite completa `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
