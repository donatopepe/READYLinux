# Test Results

## 2026-10-18 — QEMU cmdline gate baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a6af4f7cd67d341b4ad4bf3d3bb7e2b5406b53fb`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Static status guard checks firing HEAD and host BitBake/QEMU limitations.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path uses fake tools, not a real boot; no real Yocto parse/build.
