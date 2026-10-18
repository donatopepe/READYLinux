# Risultati test

## 2026-10-18 — Validazione locale unità systemd

- `bash scripts/validate-systemd-unit.sh` su WSL Debian 13/systemd 257 — PASS; nessun warning/error.
- Script sostituisce solo in copia temporanea `ExecStart` con `/bin/true`; sorgente versionato non modificato. Non è test d'integrazione image/boot.
- `python -m unittest tests.test_systemd_validation_script -v` — PASS, 3 test.
- Windows/Python 3.11 suite — PASS, 62 test; WSL Debian 13/Python 3.13 suite — PASS, 62 test.
- Compileall e shell syntax su entrambi — PASS; `git diff --check` — PASS.
