# Risultati test

## 2026-10-18 — Baseline QEMU cmdline validator

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `b4ebeeec1e4f6aa2271771ac56ca03d76c5c4948`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression statica status verifica firing HEAD, suite count e limiti BitBake/QEMU bilingui.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path testato con fake tools; nessun boot reale, parse/build Yocto reale non eseguiti.
