# Test Results

## 2026-10-18 — Offline static Yocto regressions

- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression tests cover runtime `file://` resolution within the repo, console `FILESEXTRAPATHS` search paths, and exact non-duplicated equality of `IMAGE_INSTALL` with runtime/console packages.
- Targeted Windows/WSL tests PASS; full suite: 117 tests PASS (8 platform-specific skips) on both.

## 2026-10-18 — Initial host-preflight snapshot

- `git status --short --branch`: `main...origin/main`; untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `0338faf776a825d08554cd40604098a3125a168a`.
- Read-only WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
