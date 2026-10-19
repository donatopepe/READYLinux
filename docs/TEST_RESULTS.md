# Risultati test

## 2026-10-18 — Baseline QEMU cmdline gate

- Snapshot iniziale firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4acff587a5d1867d0f33abae0e732a38d7a60d07`.
- Storico WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard status statico controlla firing HEAD, conteggio suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative gate verificato con fake tools; nessun boot reale, nessun BitBake parse/build.
