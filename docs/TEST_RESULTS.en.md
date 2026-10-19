# Test Results

## 2026-10-18 — QEMU gate snapshot

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `e9c91f50ff3eafcc5c6b18145c844c96b9e63f63`.
- Historical WSL security assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard protects firing HEAD, suite count and BitBake/QEMU limits in IT/EN files.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Negative QEMU cmdline test uses fake tools; no real boot. No Yocto parse/build.
