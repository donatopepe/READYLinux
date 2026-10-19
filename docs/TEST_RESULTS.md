# Risultati test

## 2026-10-18 — Baseline helper artifact

- Host probe test stubs every required command and supplies an existing BUILDDIR; checks clean completion without claiming BitBake parse.
- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `7b052859821ad357e77aa89b8f580bb78a2dd1e7`.
- WSL systemd hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression test statico impone HEAD, baseline e limiti host nei status IT/EN.
- Windows/Python 3.11: 104 test PASS (3 skip platform-specific); WSL Debian 13/Python 3.13: 104 test PASS.
- Verifier input audit covers missing/empty files and a non-empty directory named with image suffix; the directory is still rejected.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun parse/build BitBake/Yocto o boot QEMU reale.
