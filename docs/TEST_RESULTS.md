# Risultati test

## 2026-10-18 — Baseline validazione QEMU

- Snapshot iniziale firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `29c00fd7bfd555238f5c780e63c906f19bfff672`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status verifica firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- QEMU input-validation test usa tool fake; nessun boot reale. Nessun parse/build Yocto reale.
