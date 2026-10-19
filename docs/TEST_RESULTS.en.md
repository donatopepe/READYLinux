# Test Results

## 2026-10-18 — Host preflight baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a1d1f330b046f9146350ce5dc3ba125a09ad5a16`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Static test checks HEAD hash, baseline and host limitations reported by the IT/EN status files.
- Windows/Python 3.11: 108 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 108 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positive/negative scenarios tested with stubs; no install, fetch, BitBake parse/build or real QEMU boot.
