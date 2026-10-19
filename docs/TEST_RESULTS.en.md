# Test Results

## 2026-10-18 — Yocto recipe guard snapshot

- Yocto validator regression accepts a valid build path with spaces on WSL; Windows skips because temp dirs are outside WSL filesystem.
- Firing-start snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `c71d630a4a651dd8acb7ec6821a06e66c12f7c11`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test guards HEAD, suite baseline and BitBake/QEMU limitations in IT/EN status.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Recipe-source inventory checked statically. No real BitBake parse/build or QEMU boot.
