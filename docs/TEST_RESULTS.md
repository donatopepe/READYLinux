# Risultati test

## 2026-10-18 — QEMU cmdline rejection baseline

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `b602c42b327ac8d065944fd21e9a58b2bb32b44b`.
- Prior WSL security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status controlla firing HEAD, suite count e limiti BitBake/QEMU.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU invalid/missing-cmdline test uses fake tools and verifies they are not called. No QEMU boot, BitBake parse/build or image build.
