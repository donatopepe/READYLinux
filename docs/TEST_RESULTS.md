# Risultati test

## 2026-10-18 — Hardware guidance documentation baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `e07025bf1b89ca7e6926dae78a0db884100a143f`.
- WSL systemd hardening finding storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status guarda firing HEAD, conteggio test e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- README e docs collegano guida hardware bilingual capacity-estimate; nessuna web research/download/inferenza reale eseguita. Nessun parse/build Yocto o boot QEMU reale.
