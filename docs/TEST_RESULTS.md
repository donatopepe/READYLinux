# Risultati test

## 2026-10-18 — Record example evidenze

- Aggiunto `docs/YOCTO_BUILD_EVIDENCE.example.json`, record esplicitamente non buildato/non verificato.
- Schema Draft 2020-12 ora richiede `deviations`; test controlla keys top-level allineate e stati not-run.
- Test schema/example — PASS; suite `python -m unittest discover -s tests -v` — PASS, 58 test.
- compileall, `bash -n`, `git diff --check` — PASS.
