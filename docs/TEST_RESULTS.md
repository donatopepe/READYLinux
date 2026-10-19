# Risultati test

## 2026-10-18 — Baseline QEMU SSH opt-in test

- Regression: optional SSH forwarding is accepted only as `hostfwd=tcp:127.0.0.1:2222-:22`; default QEMU networking stays disabled.
- Firing start snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`.
- Snapshot firing start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`.
- WSL systemd hardening historique: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status static test tutela firing HEAD e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- QEMU SSH port-forward test fake verifica solo bind host-loopback e arg gating; nessun servizio SSH guest/image boot verificati. Nessun parse/build Yocto reale.
