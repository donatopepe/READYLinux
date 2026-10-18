# Risultati test

## 2026-10-18 — Helper validation Yocto

- `bash -n scripts/validate-yocto-env.sh` — PASS.
- `python -m unittest tests.test_yocto_validation_script -v` — PASS, 3 test.
- `bash scripts/validate-yocto-env.sh` senza `BUILDDIR` — exit 2 previsto, nessun fetch/build avviato.
- `python -m unittest discover -s tests -v` — PASS, 46 test; compileall, shell syntax (`install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh`) e `git diff --check` — PASS.
- BitBake non installato; parse reale non eseguito.
