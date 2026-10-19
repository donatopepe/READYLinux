# Test Results

## 2026-10-18 — Observed Yocto prerequisite blockers

- Historical WSL systemd hardening assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Current firing snapshot is recorded in this file and guarded by the static status test.
- Read-only `bash scripts/check-yocto-host.sh`: exit 1; Debian 13/trixie x86_64, 20 CPUs; all 19 required host commands found; QEMU+sha256sum found; BitBake/bitbake-layers absent; BUILDDIR unset; no package changes.
- Added `docs/VERIFICATION_PLAN.md`, breaking open status gaps into gated prerequisites, commands and acceptance evidence. No install, clone, network, parse or build performed.
- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `4ecf470a867f391f22c5f257c661df6a229242f3`.
- WSL read-only host preflight: exit 1 (`INCOMPLETE`), 19 required commands OK, `qemu-system-x86_64`/`sha256sum` found, `bitbake`/`bitbake-layers` absent, `BUILDDIR` unset; no package changes. No network/install/clone attempted. Gate A remains blocked until a release-pinned OE host exists.
- Static status regression protects firing HEAD, suite count and BitBake/QEMU limits in both languages.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Fake-QEMU tests verify loopback-only SSH forwarding, networking off by default, and invalid ports rejected before invocation. Guest SSH/real boot/Yocto build not tested.
