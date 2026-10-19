# Test Results

## 2026-10-18 — WSL Yocto preflight baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `ffe6d5b6563c42baaecac7de738767cc2b6089f5`.
- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- WSL read-only host probe: exit 1 `INCOMPLETE`; 19/19 required commands OK; QEMU+sha256sum present; BitBake/bitbake-layers absent; BUILDDIR unset; no package changes.
- Status regression checks firing HEAD, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No BitBake parse/build, image build or real QEMU boot.
