# Risultati test

## 2026-10-18 — Baseline verificata al firing

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json` non tracciato; HEAD `7fbe08e17072d45c070c847b14825097228f3dfe`.
- Finding systemd storico WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati allo snapshot; test statico controlla HEAD, test count e limiti host.
- Windows/Python 3.11: 99 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 99 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check` — PASS su entrambi.
- Nessun parse/build Yocto, package QA o boot QEMU reale; BitBake assente.
