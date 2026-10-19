# Test Results

## 2026-10-18 — WSL Yocto preflight evidence baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `433928a503e426512b5415ec6bb77a0d73314230`.
- Historical WSL hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- WSL host probe is read-only: exit 1 `INCOMPLETE`; 19/19 required commands OK, QEMU+sha256sum found, BitBake/bitbake-layers and BUILDDIR absent. No install/fetch.
- Static status regression checks firing HEAD, test count and BitBake/QEMU limits.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No BitBake parse/build, image build, QEMU boot or guest SSH run.
