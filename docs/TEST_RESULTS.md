# Risultati test

## 2026-10-18 — Baseline artifact verification → fake boot

- HEAD iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `ea9ad866c04453ef67ba5b9a8c8e25294917aba4`.
- Report WSL storico systemd: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN riallineati al firing-start HEAD; test statico controlla hash snapshot, test count e limiti host.
- Windows/Python 3.11: 101 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 101 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun Yocto/BitBake parse/build, package QA o boot QEMU reale.
