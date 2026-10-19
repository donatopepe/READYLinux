# Test Results

## 2026-10-18 — Artifact helper baseline

- Initial snapshot: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `498d96875365fa45ec895bb23b6f46e7168875ee`.
- Historical WSL systemd hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test requires HEAD, baseline and host limits in IT/EN status.
- Windows/Python 3.11: 103 tests PASS (2 skips: `systemd-analyze`, POSIX FIFO); WSL Debian 13/Python 3.13: 103 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No BitBake/Yocto parse/build or real QEMU boot.
