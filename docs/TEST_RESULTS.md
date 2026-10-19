# Risultati test

## 2026-10-18 — Baseline ricette Yocto

- Snapshot firing iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `bd7b76164f1008657ba9def973fa2736e56ea986`.
- Storico WSL systemd security: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test status statico protegge firing HEAD, conteggio suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Application recipe `file://` source guard locale; BitBake non disponibile: nessun parse/build reale, nessun download.
