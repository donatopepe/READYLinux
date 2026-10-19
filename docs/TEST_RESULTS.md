# Risultati test

## 2026-10-18 — Baseline QEMU input gate

- Snapshot firing iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `b7d1cdfb2cff97e86fe692c353078f9fd6ec1cb0`.
- Storico WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status verifica snapshot/head, conteggio test e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- QEMU cmdline negative test esercita il gate con fake tools; nessun boot reale o Yocto parse/build.
