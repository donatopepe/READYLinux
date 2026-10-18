# Risultati test

## 2026-10-18 — Schema machine-readable evidenze Yocto

- Aggiunto `docs/YOCTO_BUILD_EVIDENCE.schema.json` Draft 2020-12, senza dipendenze Python aggiuntive.
- Test `json.loads` e sezioni/audit fields richiesti — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
- Nessun dato o risultato build inventato.
