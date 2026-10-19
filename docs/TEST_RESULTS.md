# Risultati test

## 2026-10-18 — Verifica verifier artifact

- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` non tracciati; `git log -1` = `71610716030e5a02cbb2ad0839b946cba1387f89`.
- Finding WSL precedente `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Test statico verifica snapshot, baseline e limiti host riportati negli status IT/EN.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze`, FIFO Unix non supportata); WSL Debian 13/Python 3.13: 103 test PASS.
- `compileall`, `python -m unittest discover -s tests -v`, `bash -n` scripts e `git diff --check` eseguiti.
- Test FIFO conferma `is_fifo()`, rifiuto nonbloccante da verifier; nessuna lettura FIFO.
- Nessun BitBake/Yocto parse/build o QEMU reale.
