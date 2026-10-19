# Risultati test

## 2026-10-18 — Yocto validator path-space baseline

- QEMU helper negative-path regression checks a verified fixture plus empty `READY_QEMU_APPEND`; it returns a config error without invoking fake QEMU tools.
- Snapshot start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`.
- Storico systemd WSL: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status protegge snapshot/head e limiti BitBake/QEMU.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Spaced-BUILDDIR validator happy path esegue solo BitBake fake su WSL; Windows skip per temp path non condiviso. Nessun parse/build reale.
