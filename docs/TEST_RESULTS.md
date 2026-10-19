# Risultati test

## 2026-10-18 — Baseline firing e static audit

- Full-suite command: `python -m unittest discover -s tests -v`.
- HEAD iniziale: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; `git log -1` = `81298d7dc97c40ab96ac39725d9a0b720b086320`.
- Status IT/EN aggiornati allo snapshot; test statico protegge hash, baseline e limiti host.
- Windows/Python 3.11: 98 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 98 test PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` scripts; `git diff --check` passano su entrambi.
- WSL systemd security measurement storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- No BitBake/Yocto parse/build o QEMU boot reali; host manca BitBake e nessun checkout release-pinned è presente.
