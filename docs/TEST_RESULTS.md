# Risultati test

## 2026-10-18 — QEMU gate baseline

- Snapshot start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `8e838f6eb2420c16ca26f06e970850bbbb616f23`.
- Historical WSL systemd security output: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status check guarda snapshot HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- QEMU cmdline failure-before-tools usa tool fake; nessun boot reale, nessun Yocto parse/build.
