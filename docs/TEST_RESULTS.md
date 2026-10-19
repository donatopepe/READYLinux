# Risultati test

## 2026-10-18 — QEMU cmdline gate baseline

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `a6af4f7cd67d341b4ad4bf3d3bb7e2b5406b53fb`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Status guard statico controlla firing HEAD e limiti host BitBake/QEMU.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative-path test usa fake tool e non effettua boot; nessun parse/build Yocto reale.
