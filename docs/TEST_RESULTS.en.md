# Test Results

## 2026-10-18 — Firing baseline and documentation verification

- New QEMU COW failure-path test verifies nonzero QEMU exit propagates and temporary overlay is cleaned up.
- Verified initial snapshot: `git status --short --branch` was `main...origin/main` plus untracked `.pi-loop.json`; HEAD `23a77ce153a5bfcd347a394c26273d7a3dd4d8b3`.
- Complete Windows/Python 3.11 and WSL Debian 13/Python 3.13 suites: 100 tests PASS (1 systemd-analyze skip); compileall/shell syntax/diff-check PASS.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Static test checks snapshot, test count, and BitBake/QEMU limitations in IT/EN status.
- Windows/Python 3.11 suite: 100 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13 suite: 100 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No Yocto build/BitBake parse or real QEMU boot performed.
