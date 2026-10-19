# Risultati test

## 2026-10-18 — Yocto validator path spaces

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `1ab9e0ce3dbec67cb9b7a201f254e55c5945cbec`.
- Historical WSL hardening assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test protegge firing HEAD, suite count e limiti BitBake/QEMU nei status IT/EN.
- Windows/Python 3.11: 110 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 110 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Validatore Yocto con BUILDDIR contenente spazi PASS WSL con BitBake fake; scenario skip Windows perché path temporanei Windows non sono nel filesystem WSL. Parse reale non eseguito.
