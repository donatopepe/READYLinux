# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `d3b21733de5299dae53fcf4c75e021481ff7883b`.
- Historical WSL systemd hardening output: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe preflight WSL read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica ai pacchetti.
- Status static regression protegge HEAD, conteggio suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto, build image o boot QEMU reale.
