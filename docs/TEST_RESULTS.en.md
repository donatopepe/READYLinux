# Test Results

## 2026-10-18 — Host preflight snapshot baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `141f86a6893e77903096b2bddc5556ffeca52c7c`.
- Historical WSL `systemd-analyze security --offline` finding: MEDIUM/6.7, UMask 0027.
- Static test requires HEAD, test count and BitBake/QEMU limits in IT/EN status.
- Windows/Python 3.11: 105 tests PASS (4 platform-specific skips); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Positive and file-BUILDDIR-negative host probe paths tested with stubs; no install, fetch or real BitBake parse/build.
