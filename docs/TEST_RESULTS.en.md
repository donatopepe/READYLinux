# Test Results

## 2026-10-18 — Host preflight snapshot baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `758d9ddf597d19e258ed00c86570a414347ec6ce`.
- Historical WSL `systemd-analyze security --offline` finding: MEDIUM/6.7, UMask 0027.
- Static test requires HEAD, test count and BitBake/QEMU limits in IT/EN status.
- Status docs and guards were synchronized during this firing; application suite results follow.
- Windows/Python 3.11: 105 tests PASS (4 platform-specific skips); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Positive and file-BUILDDIR-negative host probe paths tested with stubs; no install, fetch or real BitBake parse/build.
