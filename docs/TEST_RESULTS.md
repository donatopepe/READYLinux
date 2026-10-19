# Risultati test

## 2026-10-18 — Baseline artifact verifier

- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `dbad747059f7fce6304ad2c267d8ce6444572ceb`.
- Finding systemd WSL storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN snapshot guard controlla HEAD, baseline test e limiti BitBake/QEMU.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze`, FIFO POSIX non supportata); WSL Debian 13/Python 3.13: 103 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier rifiuta FIFO Unix non bloccando; skip Windows atteso. Nessun parse/build Yocto o boot QEMU reale.
