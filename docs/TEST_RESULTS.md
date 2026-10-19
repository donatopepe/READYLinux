# Risultati test

## 2026-10-18 — Baseline verificata al firing

- Full-suite command: `python -m unittest discover -s tests -v`.
- Snapshot d'inizio: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json` non tracciato; HEAD `0c7196213755826a75c7f3a55b023d180e2772eb`.
- Osservazione WSL precedente `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati a tale snapshot; test statico controlla hash, baseline e limiti host.
- Windows/Python 3.11: 97 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 97 test PASS.
- Comandi verificati: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts e `git diff --check` superati su entrambi.
- BitBake/Yocto parse/build e boot QEMU reali non eseguiti.
