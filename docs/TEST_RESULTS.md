# Risultati test

## 2026-10-18 — Artifact verifier baseline

- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `923e397c3e0d9e7f3b3805731fae95b462f7cc86`.
- Report storico WSL unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test status statico richiede hash HEAD, baseline test e limiti host in entrambi gli status.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze`, FIFO Unix non supportata); WSL Debian 13/Python 3.13: 103 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- FIFO artifact verifier: WSL test PASS, FIFO identificata e rifiutata senza lettura; skip atteso su Windows.
- Nessun BitBake/Yocto parse/build o boot QEMU reale.
