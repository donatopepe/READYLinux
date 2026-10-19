# Test Results

## 2026-10-18 — QEMU guard firing baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `ec5f0817b446e266718661713d6d15965c71a985`.
- Historical WSL finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test checks snapshot HEAD, test count and BitBake/QEMU limitations in IT/EN.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative-path checked using fake tools only; no real boot or Yocto parse/build.
