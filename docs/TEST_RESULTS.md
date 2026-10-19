# Risultati test

## 2026-10-18 — Baseline path-space Yocto

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `d5bb2bab37fdcc99d364d1fc4eed9ce67e928da2`.
- Historical WSL hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression test statico copre firing HEAD, count test e limiti BitBake/QEMU negli status bilingui.
- Windows/Python 3.11: 110 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 110 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Happy path validator con BUILDDIR contenente spazi usa un BitBake fake; PASS WSL, Windows skip POSIX path scenario. Parse/build reale non eseguito.
