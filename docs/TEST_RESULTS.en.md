# Test Results

## 2026-10-18 — Firing baseline and documentation verification

- Verified initial snapshot: `git status --short --branch` was `main...origin/main` plus untracked `.pi-loop.json`; HEAD `6778a88adf74563db15223c882a492d2a22f0226`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Static test checks snapshot, test count, and BitBake/QEMU limitations in IT/EN status.
- Windows/Python 3.11 suite: 99 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13 suite: 99 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No Yocto build/BitBake parse or real QEMU boot performed.
