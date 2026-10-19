# Risultati test

## 2026-10-18 — Snapshot host-preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `665bd248b024a99aa064182bd925142e9387e41b`.
- Historical WSL security assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- WSL host probe read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Regression status controlla firing HEAD, suite count e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o boot QEMU reale.
