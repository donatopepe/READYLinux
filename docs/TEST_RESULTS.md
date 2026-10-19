# Risultati test

## 2026-10-18 — Snapshot host-preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `6b80686c69b6cfc994300b126e7adc4eba5cf707`.
- Historical WSL systemd-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe host preflight WSL read-only: exit 1 `INCOMPLETE`; 19/19 required comandi presenti, BitBake/bitbake-layers e BUILDDIR assenti; no package changes.
- Regression status statica tutela firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse/build, image build, QEMU boot reale.
