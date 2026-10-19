# Risultati test

## 2026-10-18 — Baseline documentazione hardware

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `5b405a49bbb493a8235ddc33622a48a2465381f3`.
- Previous WSL systemd hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico verifica HEAD, conteggio test e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- README, roadmap e architettura linkano guida hardware AI bilingue e dichiarano limiti ricerca/performance. Nessuna web query/download eseguiti.
- No real Yocto parse/build or QEMU boot.
