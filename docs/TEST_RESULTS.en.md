# Test Results

## 2026-10-18 — Host preflight baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `0daac11d2eb3cd47e02bdd4984d10339cfe2a968`.
- Historical WSL systemd security finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static guard checks HEAD, test count and BitBake/QEMU limitations in IT/EN status.
- Windows/Python 3.11: 105 tests PASS (4 skips: `systemd-analyze` plus three POSIX/PATH cases); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host probe positive/negative paths use command stubs; no installation, fetch or real BitBake parse/build.
