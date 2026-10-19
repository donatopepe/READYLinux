# Risultati test

## 2026-10-18 — Host preflight baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `0daac11d2eb3cd47e02bdd4984d10339cfe2a968`.
- Finding WSL systemd security storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico verifica HEAD, conteggio test e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 105 test PASS (4 skip: `systemd-analyze` e tre test POSIX/PATH); WSL Debian 13/Python 3.13: 105 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host probe: positive/negative path con command stubs; nessuna installazione, fetch o parse/build BitBake reale.
