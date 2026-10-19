# Test Results

## 2026-10-18 — QEMU fake-tool regression baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `89813789130d06875c045f4216ba2add142b8ff6`.
- Historical WSL systemd hardening check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test checks firing HEAD, suite count and BitBake/QEMU limits in IT/EN.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path uses fake tools and asserts no invocation; no real boot/Yocto parse-build.
