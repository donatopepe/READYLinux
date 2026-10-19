# Risultati test

## 2026-10-18 — WSL host-preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `cca357e318ced2618e146bc1eaf6ccdbe97b739c`.
- Historical WSL systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host probe WSL read-only: exit 1 `INCOMPLETE`, 19/19 required commands presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Static regression status protegge HEAD, test count e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build BitBake, boot QEMU o inferenza reale.
