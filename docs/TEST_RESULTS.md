# Risultati test

## 2026-10-18 — Baseline layer Yocto

- Snapshot firing iniziale: `git status --short --branch` era `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `f958f291a97176bc9f8ad8f2286edf61adca77e0`.
- Historical WSL systemd unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati; test statico controlla firing HEAD, conteggio test e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Recipe inventory e sorgenti `file://` verificabili staticamente; nessun parse/build BitBake o boot QEMU reale.
