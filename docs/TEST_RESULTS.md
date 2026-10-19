# Risultati test

## 2026-10-18 — Baseline artifact verifier firing

- HEAD iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `d622f96c46ca34da204bc42090b97254eeedabee`.
- WSL hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico controlla status snapshot/baseline e dichiarazione limiti BitBake/QEMU.
- Windows/Python 3.11: 101 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 101 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier: digest valido/mismatch, forma input, file mancante/vuoto, symlink/path spaziato; nessuna mutazione artifact.
- BitBake/Yocto parse/build e boot QEMU reale non eseguiti.
