# Risultati test

## 2026-10-18 — Baseline status hardware guidance

- Snapshot firing: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `1aaa8c5b882ae04e3d1f70c1be32731b47191e25`.
- Historical WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status controlla HEAD/hash, count test e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Hardware guide IT/EN dichiarata stima capacity-based; ricerca web/download non effettuati. BitBake/Yocto e boot QEMU non disponibili.
