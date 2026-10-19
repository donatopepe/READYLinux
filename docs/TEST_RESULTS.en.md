# Test Results

## 2026-10-18 — Offline Yocto recipe-closure checks

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Static regressions cover runtime `file://` resolution beneath repository root, console `FILESEXTRAPATHS` service lookup, and exact `IMAGE_INSTALL` equality to runtime and console package names.
- Targeted Windows/WSL tests PASS; full suite PASS: 117 tests (8 platform skips) on both.

## 2026-10-18 — Firing-start WSL preflight snapshot

- `git status --short --branch`: `main...origin/main`; untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `c4f4129d76f00c42214edcef632a3e417bfea1f1`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
