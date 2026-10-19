# Risultati test

## 2026-10-18 — Yocto preflight firing baseline

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json`/`raw` (0 byte) non tracciati; `git log -1` = `afc7962efca1f8c28819e57e340df881ac092299`.
- Finding WSL unit hardening storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati; test statico controlla firing-start HEAD, conteggio baseline e limiti BitBake/QEMU.
- Windows/Python 3.11: 105 test PASS (4 skip platform-specific); WSL Debian 13/Python 3.13: 105 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive e negative BUILDDIR testati via stub; nessuna installazione/fetch/parse-build reale.
