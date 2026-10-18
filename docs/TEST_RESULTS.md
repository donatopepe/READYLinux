# Risultati test

## 2026-10-18 — Integrità storico evidenze

- Template IT/EN richiedono run ID unico e append-only: nuovi record per tentativo; correzioni via nuovo record che referenzia precedente.
- Test statico verifica policy in entrambi i template.
- `python -m unittest discover -s tests -v` — PASS, 59 test; compileall, `bash -n`, `git diff --check` — PASS.
- Nessun record/build reale creato.
