# Test Results

## 2026-10-18 — Host-preflight snapshot baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `6bcfb1c5c3d146156d070ee3adcbd2d8f8df92c2`.
- Previous WSL systemd-hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression requires HEAD, suite count and BitBake/QEMU limits in IT/EN status.
- Prior WSL unit-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Windows/Python 3.11: 108 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 108 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive/negative BUILDDIR cases tested with stubs; no install/fetch/real parse/build.
