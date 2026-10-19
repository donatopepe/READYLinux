# Risultati test

## 2026-10-18 — Baseline hardware documentation

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4a3c4da1e8339070f7a388247340c810bed87332`.
- Finding WSL storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico verifica snapshot e conteggio/limiti BitBake/QEMU documentati.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Hardware recommendation policy aggiornata senza web research (no browser/search tool; network non consentita). Capacità indicative, non benchmark, requisiti o SKU verificati.
- Nessun modello scaricato; nessuna inferenza reale o build/boot Yocto/QEMU.
