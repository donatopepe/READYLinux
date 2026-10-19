# Risultati test

## 2026-10-18 — Snapshot gate QEMU

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `e9c91f50ff3eafcc5c6b18145c844c96b9e63f63`.
- Historical WSL hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status static guard tutela firing HEAD, conteggio suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Negative QEMU cmdline test usa tool fake; nessun boot reale. Nessun parse/build Yocto reale.
