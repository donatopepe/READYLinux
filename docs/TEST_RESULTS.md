# Risultati test

## 2026-10-18 — Host preflight baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `a1d1f330b046f9146350ce5dc3ba125a09ad5a16`.
- Finding WSL storico `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Test statico verifica l'hash HEAD, baseline e limiti host riportati negli status IT/EN.
- Windows/Python 3.11: 108 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 108 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positivo/negativo testato con stub; nessuna installazione, fetch, parse/build BitBake o boot QEMU reale.
