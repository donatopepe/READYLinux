# Test Results

## 2026-10-18 — QEMU cmdline gate baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `4acff587a5d1867d0f33abae0e732a38d7a60d07`.
- Historical WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard checks firing HEAD, suite count and BitBake/QEMU limitations in both languages.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative gate tested with fake tools; no real boot or BitBake parse/build.
