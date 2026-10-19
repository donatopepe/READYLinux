# Risultati test

## 2026-10-18 — Baseline recipe-source guard

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `f9096be2569f10d7bd2d150d8e639ca751475fcf`.
- Finding WSL systemd-security storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status protegge firing HEAD, conteggio suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Application recipe `file://` inventory staticamente verificato; nessun BitBake parse/build o boot QEMU reale.
