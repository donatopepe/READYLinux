# Test Results

## 2026-10-18 — WSL host-preflight snapshot

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `6b80686c69b6cfc994300b126e7adc4eba5cf707`.
- Historical WSL systemd-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host preflight exit 1 `INCOMPLETE`; 19/19 required host commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression protects firing HEAD, suite count and BitBake/QEMU constraints.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse/build, image build or real QEMU boot.
