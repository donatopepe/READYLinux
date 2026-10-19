# Risultati test

## 2026-10-18 — Snapshot baseline host-preflight

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `fe44fbfac3186ba7896afa45dee7c4a491f173dd`.
- Historical WSL systemd hardening assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe WSL host read-only exit 1 `INCOMPLETE`: 19/19 required commands presenti, QEMU+sha256sum presenti, BitBake/bitbake-layers e BUILDDIR assenti, no package changes.
- Static status guard tutela HEAD, count test e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun install/fetch, BitBake parse/build, image build o QEMU boot reale.
