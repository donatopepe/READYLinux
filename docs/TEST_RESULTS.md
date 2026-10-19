# Risultati test

## 2026-10-18 — QEMU guard firing baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `ec5f0817b446e266718661713d6d15965c71a985`.
- Storico WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status verifica snapshot HEAD, numero test e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- QEMU cmdline negative-path provato con tool fake; nessun boot reale né Yocto parse/build.
