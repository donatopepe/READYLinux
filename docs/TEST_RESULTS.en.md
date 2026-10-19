# Test Results

## 2026-10-18 — QEMU cmdline rejection baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `b602c42b327ac8d065944fd21e9a58b2bb32b44b`.
- Prior WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard checks firing HEAD, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU invalid/missing-cmdline tests use fake tools and confirm they are not called. No QEMU boot, BitBake parse/build or image build.
