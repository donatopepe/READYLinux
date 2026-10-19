# Risultati test

## 2026-10-18 — Baseline helper artifact

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `498d96875365fa45ec895bb23b6f46e7168875ee`.
- WSL systemd hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression test statico impone HEAD, baseline e limiti host nei status IT/EN.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze`, FIFO POSIX); WSL Debian 13/Python 3.13: 103 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun parse/build BitBake/Yocto o boot QEMU reale.
