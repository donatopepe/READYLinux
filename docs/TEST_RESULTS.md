# Risultati test

## 2026-10-18 — WSL preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `0dfec037924e8becfde35b592bf7ff9b249d7918`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Host preflight WSL read-only: exit 1 `INCOMPLETE`, 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica ai pacchetti.
- Test statico status verifica firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o boot QEMU reale.
