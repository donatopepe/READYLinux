# Risultati test

## 2026-10-18 — Baseline test/status

- Commands: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` scripts; `git diff --check`.
- Snapshot iniziale del firing verificato: `git status --short --branch` mostrava `main...origin/main`; HEAD `0d269c5ea2e8802305dce819c4899e631e049579`, `.pi-loop.json` non tracciato.
- Security report systemd WSL storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN citano lo snapshot iniziale; test statico verifica snapshot, conteggio test, limiti BitBake/QEMU.
- Baseline verificata: 97 test Windows/Python 3.11 (1 skip `systemd-analyze`) e 97 test WSL Debian 13/Python 3.13.
- `compileall`, shell syntax e `git diff --check` passano su entrambi.
- Nessun parse/build Yocto, package QA o boot QEMU reale.
