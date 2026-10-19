# Risultati test

## 2026-10-18 — Snapshot guard recipe Yocto

- Yocto env validator regression accepts a valid build directory containing spaces on WSL; Windows skips because its temp path is outside the WSL filesystem.
- Snapshot firing start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `c71d630a4a651dd8acb7ec6821a06e66c12f7c11`.
- Historic WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico protegge HEAD, suite baseline e limiti BitBake/QEMU nei status IT/EN.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Recipe source inventory verificato staticamente. Nessun BitBake parse/build o QEMU boot reale.
