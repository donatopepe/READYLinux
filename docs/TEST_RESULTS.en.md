# Test Results

## 2026-10-18 — WSL host-preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `ecd65da5b45531d2e0cd1e2d757426b2a6e74bad`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe: exit 1 `INCOMPLETE`; 19/19 required commands OK; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression checks firing HEAD, suite count, and BitBake/QEMU limits.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse, image build, QEMU boot or real inference.
