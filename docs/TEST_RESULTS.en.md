# Test Results

## 2026-10-18 — WSL preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `89d9eaefe92fb24c738e651efcb49889108d53d6`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host preflight: exit 1 `INCOMPLETE`; 19/19 required commands OK; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression protects firing HEAD and BitBake/QEMU limits.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
