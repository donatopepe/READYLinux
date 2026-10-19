# Risultati test

## 2026-10-18 — WSL preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `1c0db6cfe7565e9d79408204a04f7a9b617ac765`.
- Historical WSL systemd security run: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host probe WSL read-only exit 1 `INCOMPLETE`: 19/19 required comandi presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessun package change.
- Static status test tutela firing HEAD e limiti host BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto, image build o boot QEMU reale.
