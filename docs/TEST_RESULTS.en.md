# Test Results

## 2026-10-18 — Yocto recipe closure static tests

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Offline regressions check runtime `file://` resolution to repo root, console `FILESEXTRAPATHS` service search, and exact `IMAGE_INSTALL` equality with runtime/console packages (no duplicates).
- Targeted Windows/WSL tests PASS; full suite 117 PASS (8 platform-specific skips) on both.

## 2026-10-18 — Firing-start WSL preflight snapshot

- `git status --short --branch`: `main...origin/main`; untracked `.pi-loop.json`, `raw` (0 bytes); HEAD `e1372e6799214fd26648883acc0416acae9a7c8f`.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required host commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build, or real QEMU boot.
