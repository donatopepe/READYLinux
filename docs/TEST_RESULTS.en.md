# Test Results

## 2026-10-18 — QEMU validation baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `29c00fd7bfd555238f5c780e63c906f19bfff672`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard checks firing HEAD, suite count and BitBake/QEMU limits in both languages.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU input-validation regression uses fake tools; no real boot. No Yocto parse/build.
