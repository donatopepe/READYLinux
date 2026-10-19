# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `52901d3c5d1aba4a0b01707052bb95b3d6c10f99`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- WSL read-only host probe exit 1 `INCOMPLETE`: 19/19 required commands OK; BitBake/bitbake-layers e BUILDDIR assenti, nessuna modifica pacchetti.
- Regression status statica protegge firing HEAD, count test e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse/build, image build o QEMU boot reale.
