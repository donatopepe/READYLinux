# Test Results

## 2026-10-18 — WSL host-preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `cca357e318ced2618e146bc1eaf6ccdbe97b739c`.
- Historical WSL systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression checks firing HEAD, suite count and BitBake/QEMU constraints.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse/build, QEMU boot or real inference.
