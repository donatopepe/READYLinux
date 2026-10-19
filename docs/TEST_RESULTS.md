# Risultati test

## 2026-10-18 — Baseline firing artifact verification

- HEAD iniziale: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` e `raw` non tracciati; `git log -1` = `8460bab096e72defa1301253dedbaaa8a3f09b08`.
- Report storico WSL unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status riportano snapshot, test count e limiti Yocto; test statico controlla questi campi.
- Suite Windows/Python 3.11: 101 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 101 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Artifact verifier locale copre checksum valido/errato, input non valido, symlink e path con spazi senza mutazione. Integration fake QEMU test separato.
- Nessun BitBake/Yocto parse/build, package QA o boot QEMU reale.
