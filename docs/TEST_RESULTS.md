# Risultati test

## 2026-10-18 — Baseline firing guida AI/hardware

- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `4145bd8b748250ac7f3fd0b930389409be3a3e8d`.
- WSL systemd hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- README e docs AI hardware bilingue aggiornate; ricerca web richiesta ma non avviata: nessun browser/search disponibile e regole repo vietano rete. Fasce sono stime, non SKU/prezzi o risultati benchmark.
- Test statico status protegge HEAD e limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check` pass.
- Nessun download modello/Yocto, setup o inferenza reale; parse/build Yocto e boot QEMU assenti.
