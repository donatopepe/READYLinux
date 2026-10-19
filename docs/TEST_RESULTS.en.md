# Test Results

## 2026-10-18 — Offline Yocto static regression

- Historical WSL unit-hardening record: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Local closure test: runtime `file://` sources resolve in repo; console `FILESEXTRAPATHS` finds service; `IMAGE_INSTALL` exactly matches the runtime and console packages, without duplicates.
- Targeted Windows/WSL tests PASS; full suite 117 PASS (8 platform-specific skips) on both.

## 2026-10-18 — Initial host-preflight snapshot

- `git status --short --branch`: `main...origin/main`; untracked `.pi-loop.json`, `raw` (0 bytes); HEAD `b3b8e74017885f1da899cabe3b60fd49c802ec91`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
