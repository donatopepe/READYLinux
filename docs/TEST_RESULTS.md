# Risultati test

## 2026-10-18 — CWD helper BitBake

- Helper invoca `bitbake -p` da `BUILDDIR` canonico, non dalla directory chiamante.
- Test happy-path usa falso eseguibile BitBake e verifica cwd; test symlink builddir e branch preflight già presenti.
- `python -m unittest discover -s tests -v` — PASS, 51 test; compileall, `bash -n` su tutti gli script e `git diff --check` — PASS.
- BitBake reale non disponibile.
