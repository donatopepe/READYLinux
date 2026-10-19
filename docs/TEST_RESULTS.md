# Risultati test

## 2026-10-18 — Baseline firing artifact/QEMU helper

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `2957a95d7d8041992f2ab3c1e9ba71ea044c828a`.
- Finding systemd storico WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico richiede che status IT/EN registrino snapshot, baseline e limiti BitBake/QEMU.
- Suite Windows/Python 3.11: 101 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 101 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` sugli script; `git diff --check`.
- Nessun parse/build BitBake/Yocto o boot QEMU reale.
