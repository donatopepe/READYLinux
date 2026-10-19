# Risultati test

## 2026-10-18 — Baseline test/status

- Existing WSL systemd security measurement: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Commands: `python -m unittest discover -s tests -v`, `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts, `git diff --check`.
- Snapshot di inizio firing verificato: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; HEAD `704a563c7d7a8252e2205304222e7ce0c0dd7384`.
- Lo snapshot storico `28f5bba753f44fe58ae5063eb93f06f470bec5bd` è mantenuto come contesto dei test statici precedenti, non come HEAD attuale.
- Distro opt-in check copre `DISTRO`, `MACHINE` placeholder, systemd init policy e service recipe autostart.
- Windows/Python 3.11: 96 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 96 test PASS.
- `compileall`, shell syntax e `git diff --check` passano su entrambi.
- Nessun BitBake/Yocto parse, build o QEMU boot reale.
