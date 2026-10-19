# Test Results

## 2026-10-18 — Offline Yocto static checks

- Historical WSL systemd hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Added source/package closure regression: runtime recipe `file://` entries must resolve under repo root, console `FILESEXTRAPATHS` must find its service, and image `IMAGE_INSTALL` must exactly match runtime and console packages without duplicates.
- Targeted test PASS on Windows/WSL; full suite PASS: 117 tests (8 platform-specific skips) on both.

## 2026-10-18 — WSL preflight snapshot

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `5f8d51aa5dfaa62996f14651ca7c7bd71a55bc61`.
- Read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Static status test protects firing HEAD and host limits.
- Windows/Python 3.11: 117 tests PASS (8 platform skips); WSL Debian 13/Python 3.13: 117 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, BitBake parse/build, image build or real QEMU boot.
