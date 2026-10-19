# Test Results

## 2026-10-18 — WSL preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `86eccd9631702a07ebc0581018d8151c2d4537ac`.
- Historical WSL systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe exit 1 `INCOMPLETE`; all 19 required commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status test guards firing HEAD and BitBake/QEMU limits.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
