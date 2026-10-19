# Test Results

## 2026-10-18 — Offline Yocto recipe regressions

- Historical WSL systemd-hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regressions verify runtime `file://` source resolution, console `FILESEXTRAPATHS` search paths, and `IMAGE_INSTALL` equality to runtime/console packages without duplicates. They invoke no BitBake or downloads.
- Targeted Windows/WSL test PASS; full suite: 117 tests PASS (8 platform-specific skips) on both.

## 2026-10-18 — Firing-start host-preflight snapshot

- Initial `git status --short --branch`: `main...origin/main`, untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `0277c37cba956daf6c830fb0d4d8b80cdc81c306`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required host commands present, BitBake/bitbake-layers/BUILDDIR absent, no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build, or real QEMU boot.
