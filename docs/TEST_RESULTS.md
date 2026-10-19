# Risultati test

## 2026-10-18 — Host-preflight snapshot baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `6bcfb1c5c3d146156d070ee3adcbd2d8f8df92c2`.
- Report WSL precedente systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression statica richiede HEAD, conteggio suite e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 108 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 108 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Host probe positive/negative con BUILDDIR testati mediante stub; nessuna installazione/fetch/parse-build reale.
