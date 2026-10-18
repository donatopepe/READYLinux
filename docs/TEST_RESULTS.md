# Risultati test

## 2026-10-18 — Negative cases schema evidenze

- Esempio JSON placeholder verificato contro campi required, shape nested, pattern commit/hash ed enum.
- Aggiunti negative assertions per commit malformed, verdict invalido e field richiesto mancante.
- Test mirato `test_build_evidence_schema_is_valid_json_with_audit_fields` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS. Nessuna libreria JSON Schema esterna usata.
