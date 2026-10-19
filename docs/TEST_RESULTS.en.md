# Test Results

## 2026-10-18 — WSL host preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `75b12e66324b51a9631754b63b03a17ebe3f0300`.
- Historical WSL hardening output: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only `bash scripts/check-yocto-host.sh`: WSL Debian 13/trixie, exit 1 `INCOMPLETE`, 19/19 required commands OK, QEMU+sha256sum found; BitBake/bitbake-layers absent, BUILDDIR unset; no package changes.
- Static status guard protects firing HEAD and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse, image build or QEMU boot.
