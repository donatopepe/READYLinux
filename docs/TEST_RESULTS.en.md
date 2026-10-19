# Test Results

## 2026-10-18 — QEMU cmdline gate baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `3fff85ca0c45b62954ff5df2fe0c0255f9daf169`.
- Historical WSL hardening check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression protects firing HEAD, suite count and BitBake/QEMU limits in IT/EN.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU fail-before-tools cmdline case uses fake tools; no real boot or Yocto parse/build.
