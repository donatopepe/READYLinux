# Test Results

## 2026-10-18 — Offline Yocto static tests

- Historical WSL unit-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Recipe-closure regression: runtime `file://` sources resolve to repository root; console `FILESEXTRAPATHS` locates the local service; image `IMAGE_INSTALL` equals exactly the runtime/console package names without duplicates.
- Targeted test PASS Windows+WSL; full suite: 117 tests PASS (8 platform skips) on both.

## 2026-10-18 — Firing-start WSL preflight snapshot

- `git status --short --branch`: `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `ff2612cc6af9639a437e5f22f6b863b985f3ff13`.
- Read-only WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; all 19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
