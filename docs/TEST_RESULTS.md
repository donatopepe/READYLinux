# Risultati test

## 2026-10-18 — Conformità esempio/schema Yocto

- Il test stdlib verifica chiavi nested, required fields, pattern SHA/commit e enum contro schema JSON; nessuna libreria validator esterna.
- Test mirato — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
- Esempio resta esplicitamente not-built/not-verified.
