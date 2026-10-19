# Test Results

## 2026-10-18 — QEMU cmdline validator baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `b4ebeeec1e4f6aa2271771ac56ca03d76c5c4948`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression checks firing HEAD, suite count and BitBake/QEMU limits in both languages.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path tested with fake tools; no real boot or Yocto parse/build.
