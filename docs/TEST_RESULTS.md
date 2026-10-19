# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `86eccd9631702a07ebc0581018d8151c2d4537ac`.
- Storico WSL systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe WSL host read-only exit 1 `INCOMPLETE`: 19/19 comandi richiesti presenti, BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Static status regression tutela firing HEAD, suite count e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto, image build o boot QEMU reale.
