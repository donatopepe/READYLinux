# Test Results

## 2026-10-18 — Yocto layer baseline

- Initial firing snapshot: `git status --short --branch` was `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `f958f291a97176bc9f8ad8f2286edf61adca77e0`.
- Historical WSL systemd-unit hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed; static test guards firing HEAD, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Recipe inventory and `file://` sources checked statically; no real BitBake parse/build or QEMU boot.
