# Risultati test

## 2026-10-18 — Preflight helper Yocto

- `python -m unittest tests.test_yocto_validation_script -v` — PASS, 7 test con fake builddir/bitbake.
- Verificati errori preflight: `BUILDDIR`, `bitbake`, `conf/bblayers.conf`, `conf/local.conf`, registrazione layer.
- Happy path chiama il fake `bitbake -p` solo dopo i controlli.
- `python -m unittest discover -s tests -v` — PASS, 50 test; compileall, `bash -n` su tutti gli script e `git diff --check` — PASS.
- Nessun parse reale o download.
