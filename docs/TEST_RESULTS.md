# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `2fa33faaa4311927fdbd788ede95f36d6e74a656`.
- Historical WSL systemd security assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe host WSL read-only: exit 1 INCOMPLETE; 19/19 required commands OK, QEMU/sha256sum presenti; bitbake/bitbake-layers/BUILDDIR assenti.
- Static status guard protegge firing HEAD, count suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No install/fetch, BitBake parse, image build, QEMU boot o inference reale.
