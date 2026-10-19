# Risultati test

## 2026-10-18 — Baseline host probe WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `e35f40e014b706e04f53cf09eaed0b37d12fdf2f`.
- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host preflight WSL read-only: exit 1 INCOMPLETE, 19/19 comandi required OK; BitBake/bitbake-layers e BUILDDIR assenti; QEMU/sha256sum presenti; nessuna modifica pacchetti.
- Static regression status verifica HEAD, conteggio test, limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse, image build, QEMU boot o inference reale.
