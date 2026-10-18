# Risultati test

## 2026-10-18 — Validazione locale unità systemd

- `systemd-analyze verify` WSL Debian 13/systemd 257 — PASS usando copia temporanea con ExecStart sostituito; unità originale non alterata.
- Test helper che verifica errore quando systemd-analyze non disponibile ora passano sia Windows/MSYS sia WSL.
- Suite aggiornata: 62 test Windows/Python 3.11 e 62 test WSL/Python 3.13 — PASS.
- `compileall` e `bash -n` su entrambi — PASS; `git diff --check` — PASS.

- `bash scripts/validate-systemd-unit.sh` su WSL Debian 13/systemd 257 — PASS; nessun warning/error.
- Script sostituisce solo in copia temporanea `ExecStart` con `/bin/true`; sorgente versionato non modificato. Non è test d'integrazione image/boot.
- `python -m unittest tests.test_systemd_validation_script -v` — PASS, 3 test.
- Windows/Python 3.11 suite — PASS, 62 test; WSL Debian 13/Python 3.13 suite — PASS, 62 test.
- Compileall e shell syntax su entrambi — PASS; `git diff --check` — PASS.
