# Risultati test

## 2026-10-18 — QEMU fake-tool regression baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `89813789130d06875c045f4216ba2add142b8ff6`.
- WSL systemd hardening historical check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico dello status verifica firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path usa fake tool e assert no invocation; nessun boot reale/Yocto parse-build.
