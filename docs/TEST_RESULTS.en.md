# Test Results

## 2026-10-18 — WSL preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `1c0db6cfe7565e9d79408204a04f7a9b617ac765`.
- Historical WSL systemd security run: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status test protects firing HEAD and BitBake/QEMU host limits.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
