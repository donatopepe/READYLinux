# Test Results

## 2026-10-18 — Offline Yocto contracts and regression suite

- Runtime recipe regression asserts `inherit allarch`, repository-local `file://` application sources, no model/network payload and declared Python dependencies. Distro test checks systemd is appended without removing inherited features and is selected as init manager.
- Historical WSL systemd-security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static contracts cover layer metadata and explicitly unverified compatibility candidates; local recipe sources, package closure and launcher-to-service `ExecStart`; getty-mask symlink ownership/image inclusion; READY home, persistent StateDirectory and UMask; plus preflight evidence.
- Relevant regressions pass; full suite: 126 tests PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- No BitBake metadata parse, image build or QEMU boot: BitBake/OE checkout and `BUILDDIR` are absent; no install/download performed.

## 2026-10-18 — Firing-start snapshot and host probe

- Initial snapshot verified by `git rev-parse HEAD`: `92abaae72d9023bb82718ff48e0918ebc17f4b23`; `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes).
- WSL read-only probe `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
