# Risultati test

## 2026-10-18 — Baseline QEMU cmdline gate

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `3fff85ca0c45b62954ff5df2fe0c0255f9daf169`.
- Storico hardening WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression status statica protegge firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline fail-before-tools test usa fake; nessun boot reale o parse/build Yocto.
