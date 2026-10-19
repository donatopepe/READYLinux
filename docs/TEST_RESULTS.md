# Risultati test

## 2026-10-18 — Baseline QEMU command-line gate

- Snapshot firing iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `630266eab071e744cc8b4bdc5e8f7f1d721cdb6a`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression statica protegge HEAD, count test e limiti BitBake/QEMU bilingui.
- Windows/Python 3.11: 111 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 111 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path usa tool fake e asserisce nessuna invocazione; nessun boot QEMU, parse/build Yocto reale.
