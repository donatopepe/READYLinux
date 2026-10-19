# Risultati test

## 2026-10-18 — Host preflight helper firing baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `e82e9b12b8b3c0d52d99b24cea78fa828b79a1e4`.
- Finding WSL storico systemd: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati allo snapshot; test statico verifica HEAD hash, conteggio suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 104 test PASS (3 skip platform-specific); WSL Debian 13/Python 3.13: 104 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host probe positive path testato con command stubs; nessuna installazione/fetch, nessun parse/build BitBake reale.
