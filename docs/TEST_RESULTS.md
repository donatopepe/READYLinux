# Risultati test

## 2026-10-18 — Regressioni sicurezza service Yocto

- Aggiunte asserzioni statiche su identità non-root, hardening richiesto, limiti write path, assenza capability/override privilegiati.
- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test; suite completa — PASS, 52 test.
- `compileall`, `bash -n` su tutti gli script, `git diff --check` — PASS.
- BitBake/systemd non presenti per unit validation/runtime.
