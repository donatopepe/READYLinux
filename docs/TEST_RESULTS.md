# Risultati test

## 2026-10-18 — Baseline firing e verifica documenti

- Snapshot iniziale verificato: `git status --short --branch` era `main...origin/main` più `.pi-loop.json` non tracciato; HEAD `6778a88adf74563db15223c882a492d2a22f0226`.
- Misura storica WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Test statico controlla snapshot, test count e limiti BitBake/QEMU nei status IT/EN.
- Suite Windows/Python 3.11: 99 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 99 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Build Yocto/parse BitBake e boot QEMU reali non eseguiti.
