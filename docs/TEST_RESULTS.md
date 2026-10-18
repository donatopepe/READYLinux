# Risultati test

## 2026-10-18 — Verifica artefatto immagine per QEMU

- Helper checksum immagine introdotto in `scripts/verify-image-artifact.sh`; verifica solo hash/file, non avvia QEMU.
- Windows/Python 3.11 suite — PASS, 66 test; WSL Debian 13/Python 3.13 suite — PASS, 66 test.
- Compileall e `bash -n` su entrambi — PASS; systemd-analyze verify su WSL — PASS; `git diff --check` — PASS.
- Nessuna immagine READY disponibile, quindi helper non applicato a un artefatto reale.

## 2026-10-18 — Verifica artifact image

- Aggiunto `scripts/verify-image-artifact.sh`: richiede file regolare/non vuoto e SHA-256 atteso; codice 0 match, 1 mismatch, 2 input/tool non valido. Non avvia QEMU né crea artifact.
- Testa hash match/mismatch, digest malformato, file mancante/vuoto.
- Suite Windows/Python 3.11 — PASS, 66 test; suite WSL Debian 13/Python 3.13 — PASS, 66 test.
- Compileall e shell syntax su entrambi — PASS; `git diff --check` — PASS.
- Nessuna immagine READY disponibile da verificare.
