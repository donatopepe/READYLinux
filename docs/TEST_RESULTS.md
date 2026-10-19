# Risultati test

## 2026-10-18 — Baseline test path-space

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `1cf4baf9a6144fc21774d84967f2bb378d601ab9`.
- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression test controlla firing HEAD, conteggio e limiti BitBake/QEMU.
- Windows/Python 3.11: 110 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 110 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Path-spaced BUILDDIR happy path usa fake BitBake e passa su WSL; Windows salta per path/temp non condiviso. Nessun parse/build Yocto reale.
