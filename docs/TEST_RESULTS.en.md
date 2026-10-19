# Test Results

## 2026-10-18 — Offline recipe closure regressions

- Historical WSL systemd-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression checks runtime `file://` resolution beneath repository root, console `FILESEXTRAPATHS` service lookup, and exact `IMAGE_INSTALL` package closure (no duplicates). No BitBake/downloads.
- Targeted test PASS on Windows and WSL; full suite PASS: 117 tests (8 platform skips) on both.

## 2026-10-18 — Initial host-preflight snapshot

- `git status --short --branch`: `main...origin/main`, untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `c99a6ba15f0d248d71143a6cd73ed8ee51b3efd2`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
