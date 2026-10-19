# Risultati test

## 2026-10-18 — Baseline helper artifact

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `c8ec19a0425d2566cd74fc19e44c379f0a0d9cc2`.
- WSL systemd hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression test statico impone HEAD, baseline e limiti host nei status IT/EN.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze`, FIFO POSIX); WSL Debian 13/Python 3.13: 103 test PASS.
- Verifier input audit covers missing/empty files and a non-empty directory named with image suffix; the directory is still rejected.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun parse/build BitBake/Yocto o boot QEMU reale.
