# Test Results

## 2026-10-18 — QEMU SSH opt-in test

- Optional SSH forwarding regression accepts only the loopback QEMU host mapping; default networking stays disabled. Fake tools; guest SSH/image boot not verified.
- Firing-start snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`.
- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`.
- Historical WSL systemd-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test protects firing HEAD and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU SSH port-forward test uses fake tools to check loopback binding and argument gating only; guest SSH/image boot not verified. No real Yocto parse/build.
