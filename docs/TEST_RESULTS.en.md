# Test Results

## 2026-10-18 — Yocto path-space validator baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `58eae291cecf218c3c2ca9568607e8ef89facd85`.
- Historical WSL systemd-security observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression checks firing HEAD, test count and BitBake/QEMU limits in IT/EN files.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Validator case with spaced BUILDDIR uses fake BitBake: PASS on WSL; Windows skips because temp path is not shared with WSL. No real Yocto parse/build.
