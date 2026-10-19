# Test Results

## 2026-10-18 — Offline Yocto recipe static tests

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Added recipe-closure test: runtime `file://` sources resolve under repository root; console `FILESEXTRAPATHS` finds its local service file; `IMAGE_INSTALL` exactly equals runtime and console recipe package names, with no duplicates. Catches missing sources/package drift without BitBake or download.
- Targeted tests passed on Windows and WSL; full suite: 117 tests PASS (8 platform skips) on both.

## 2026-10-18 — Initial WSL preflight snapshot

- `git status --short --branch`: `main...origin/main`, untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `10e7166ab5bcae8fec8a7366edbdd67cc51d8be8`.
- WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required host commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
