# Risultati test

## 2026-10-18 — Host-preflight snapshot baseline

- Bilingual hardware purchasing guidance added as dated capacity tiers/verification policy; live web research deferred (no browser tool available; repository rules prohibit network access). These are estimates, not tested requirements.
- Static Yocto recipe contract test verifies recipe inventory, shared MIT/checksum metadata and runtime dependencies for application/console.
- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `704cdb5e452dba805816e0f865232a28faeb2294`.
- Report WSL precedente systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression statica richiede HEAD, conteggio suite e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Host probe positive/negative con BUILDDIR testati mediante stub; nessuna installazione/fetch/parse-build reale. Nessuna ricerca web/download di hardware effettuata.
