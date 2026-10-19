# Risultati test

## 2026-10-18 — Baseline firing artifact-to-boot

- HEAD iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `0ffc5a57e1ea0d5b04534429340a0a721f3f868b`.
- Finding storico systemd WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN riallineati allo snapshot; test statico verifica hash HEAD, numero test e limiti BitBake/QEMU.
- Windows/Python 3.11: 101 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 101 test PASS.
- Verifiche: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun BitBake/Yocto parse/build o boot QEMU reale.
