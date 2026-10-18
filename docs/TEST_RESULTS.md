# Risultati test

## 2026-10-18 — Robustezza helper Yocto

- `python -m unittest tests.test_yocto_validation_script -v` — PASS, 8 test.
- Preflight controlla `BUILDDIR`, `bitbake`, config e layer registration; builddir symlink accettata tramite canonicalizzazione `pwd -P`.
- Happy path invoca solo fake `bitbake -p` dopo preflight.
- `python -m unittest discover -s tests -v` — PASS, 51 test.
- `compileall`, `bash -n` sugli script, `git diff --check` — PASS.
- BitBake reale non disponibile; metadata parse non eseguito.
