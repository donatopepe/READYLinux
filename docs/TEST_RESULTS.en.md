# Test Results

## 2026-10-18 — Host-preflight snapshot baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `fe44fbfac3186ba7896afa45dee7c4a491f173dd`.
- Historical WSL systemd hardening assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe exit 1 `INCOMPLETE`: 19/19 required commands present, QEMU+sha256sum present, BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression protects HEAD, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No install/fetch, BitBake parse/build, image build or real QEMU boot.
