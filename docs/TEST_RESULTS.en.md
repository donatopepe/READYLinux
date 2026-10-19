# Test Results

## 2026-10-18 — WSL host probe baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `e35f40e014b706e04f53cf09eaed0b37d12fdf2f`.
- Historical WSL security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host preflight: exit 1 INCOMPLETE, 19/19 required commands OK; BitBake/bitbake-layers and BUILDDIR absent; QEMU/sha256sum present; no package changes.
- Static status regression protects HEAD, test count and BitBake/QEMU limitations in both languages.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse, image build, QEMU boot or real inference.
