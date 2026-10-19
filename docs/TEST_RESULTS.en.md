# Test Results

## 2026-10-18 — QEMU gate baseline

- Firing start: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `8e838f6eb2420c16ca26f06e970850bbbb616f23`.
- Historical WSL systemd security output: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard checks snapshot HEAD, suite count and BitBake/QEMU limits in IT/EN.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline failure-before-tools uses fake tools; no real boot or Yocto parse/build.
