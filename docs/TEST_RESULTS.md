# Risultati test

## 2026-10-18 — Validazione WSL toolchain disponibile

- `wsl -d Debian -- ...`: Debian GNU/Linux 13 trixie, x86_64; 20 CPU logiche, 30 GiB RAM.
- Installati in WSL, su richiesta utente: toolchain build (`gcc`, `make`, Python/deps) e QEMU x86_64; nessun checkout Yocto/BitBake o download sorgenti di build ancora fatto.
- QEMU presente; BitBake assente. Non è stata avviata alcuna build.
- Suite unitaria passa su Windows e WSL dopo le correzioni path cross-platform: 59 test ciascuna. Comandi completi riportati sotto.

## 2026-10-18 — Test helper Yocto cross-platform

- Windows/Python 3.11: `python -m unittest discover -s tests -v` — PASS, 59 test.
- WSL Debian 13/Python 3.13: stesso comando — PASS, 59 test.
- `compileall` e `bash -n` su Windows e WSL — PASS. I fake layer path usano path canonici WSL.
- BitBake reale rimane assente.

## 2026-10-18 — Integrità artifact evidenze

- Test statici `python -m unittest tests.test_yocto_scaffold -v` — PASS, 13 test.
- Guide/template richiedono `sha256sum <artifact>`, path retention image/log e vietano commit di binari/credenziali.
- Nessun artifact immagine disponibile da hashare.
