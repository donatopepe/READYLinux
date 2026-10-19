# Risultati test

## 2026-10-18 — Yocto host-preflight baseline

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `614b1fb8964a992e358b51dd2d0bcf736f5b9a0e`.
- WSL systemd report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico richiede HEAD, conteggio baseline e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 105 test PASS (4 skip platform-specific); WSL Debian 13/Python 3.13: 105 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Preflight helper testato con stub positivi/negativi; nessuna installazione, fetch o parse/build BitBake reale.
