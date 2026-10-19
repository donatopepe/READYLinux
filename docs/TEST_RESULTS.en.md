# Test Results

## 2026-10-18 — Offline Yocto recipe-closure regression

- Historical WSL systemd-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test resolves runtime `file://` sources under repository root, verifies console `FILESEXTRAPATHS` finds its service file, and requires image `IMAGE_INSTALL` to equal runtime/console package names without duplicates. No BitBake/download.
- Targeted tests PASS Windows/WSL; full suite: 117 PASS (8 platform-specific skips) on both.

## 2026-10-18 — Host-preflight firing-start baseline

- `git status --short --branch`: `main...origin/main`, untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `65090d4bea45b8d3b86dbffff802891c7d9bb6fd`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
