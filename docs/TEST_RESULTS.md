# Risultati test

## 2026-10-18 — Baseline WSL host preflight

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `75b12e66324b51a9631754b63b03a17ebe3f0300`.
- Historical WSL hardening output: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe read-only `bash scripts/check-yocto-host.sh`: WSL Debian 13/trixie, exit 1 `INCOMPLETE`, 19/19 comandi required OK, QEMU+sha256sum found; BitBake/bitbake-layers assenti, BUILDDIR unset; no package changes.
- Static status test protegge HEAD e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse, image build o boot QEMU.
