# Test Results

## 2026-10-18 — Offline Yocto source/package closure test

- Added a static closure test: local `file://` sources must resolve at recipe search roots, and image `IMAGE_INSTALL` must equal declared runtime recipe packages. It checks missing source files/package drift without BitBake or downloads.
- Targeted test passed on Windows and WSL; full-suite results below.

## 2026-10-18 — WSL preflight snapshot

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a2b2036c63f4b8d848bd9ff80885d08cc31aaffa`.
- Historical WSL unit review: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host preflight exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status test protects firing HEAD and BitBake/QEMU limitations.
- Windows/Python 3.11: 117 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 117 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
