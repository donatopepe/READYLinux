# Test Results

## 2026-10-18 — Host preflight firing baseline

- Initial snapshot: `git status --short --branch` was `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `8ab20c823363df531c2026b6553496`.
- Historical WSL unit-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression checks snapshot/HEAD, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 108 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 108 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Stubbed host-probe positive/negative coverage includes required commands and BUILDDIR (unset, valid, or file); no installation/fetch/real BitBake parse/build.
