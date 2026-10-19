# Test Results

## 2026-10-18 — WSL host-preflight baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `84219b5afa145ecc31b9d51a0132f4f2eb86e926`.
- Historical WSL systemd hardening evidence: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test checks firing HEAD, suite count and BitBake/QEMU limits in both languages.
- Read-only WSL preflight exit 1 `INCOMPLETE`: 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR missing; no package changes.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, QEMU boot or real inference.
