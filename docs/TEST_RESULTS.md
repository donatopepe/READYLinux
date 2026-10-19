# Risultati test

## 2026-10-18 — Baseline preflight host WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `411aa5f09be1c7eb05bf2bae52c0a6b215e0569a`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico verifica snapshot HEAD, conteggio suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Probe host WSL read-only: exit 1 `INCOMPLETE`, 19/19 required commands presenti, BitBake e BUILDDIR assenti; nessuna installazione/fetch. Nessun parse/build Yocto o boot QEMU reale.
