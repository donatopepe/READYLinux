# Risultati test

## 2026-10-18 — Baseline Yocto path-space check

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `75f13937c1b5668160059a26c7cb8b222bdb35ba`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status verifica HEAD, conteggio test e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 110 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 110 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- `validate-yocto-env.sh` happy path con BUILDDIR contenente spazi PASS su WSL; BitBake fake. Windows skip: path temp non condiviso con WSL. Nessun parse Yocto reale.
