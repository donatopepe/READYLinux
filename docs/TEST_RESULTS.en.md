# Test Results

## 2026-10-18 — Path-space test baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `1cf4baf9a6144fc21774d84967f2bb378d601ab9`.
- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression test checks firing HEAD, suite count and BitBake/QEMU limits.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Spaced-BUILDDIR happy path uses fake BitBake and passes on WSL; Windows skips because the temp path is not shared. No real Yocto parse/build.
