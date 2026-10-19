# Test Results

## 2026-10-18 — WSL preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `b903d68eff4527165381a91d51680e333b9354a0`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe exit 1 `INCOMPLETE`: 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR missing; no package changes.
- Static status regression protects firing HEAD and BitBake/QEMU limits in both languages.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
