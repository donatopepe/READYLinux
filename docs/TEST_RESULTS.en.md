# Test Results

## 2026-10-18 — Verified baseline at firing start

- Initial snapshot: `git status --short --branch` showed `main...origin/main` plus untracked `.pi-loop.json`; HEAD `7fbe08e17072d45c070c847b14825097228f3dfe`.
- Historical WSL systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to this snapshot; static test checks HEAD, test count and host limitations.
- Windows/Python 3.11: 99 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 99 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check` — PASS on both.
- No Yocto parse/build, package QA, or real QEMU boot; BitBake unavailable.
