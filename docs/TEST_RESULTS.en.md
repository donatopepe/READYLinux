# Test Results

## 2026-10-18 — Static offline Yocto recipe test

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Regression test resolves runtime recipe `file://` sources to the repository root and checks console recipe `FILESEXTRAPATHS` search paths. It also requires image `IMAGE_INSTALL` to match exactly the declared runtime and console packages, catching missing sources or package-name drift without BitBake or downloads.
- Targeted test passed on Windows and WSL; full suite: 117 tests PASS (8 platform-specific skips) on both.

## 2026-10-18 — Initial host-preflight snapshot

- Firing-start `git status --short --branch`: `main...origin/main`, with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `9c1211592da48bd8f43e87a7d4cff1565a87abe6`.
- WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
