# Risultati test

## 2026-10-18 — WSL host preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `c17d730cb3719503529404246ba38194d4ed8d55`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host preflight WSL read-only exit 1 `INCOMPLETE`: 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; QEMU/sha256sum presenti; nessun package change.
- Static status regression protegge firing HEAD, count suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o QEMU boot reale.
