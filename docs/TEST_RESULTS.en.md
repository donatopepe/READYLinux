# Test Results

## 2026-10-18 — QEMU input-gate baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `b7d1cdfb2cff97e86fe692c353078f9fd6ec1cb0`.
- Historical WSL systemd security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression checks firing snapshot/HEAD, test count, and BitBake/QEMU limits in IT/EN.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative test exercises the gate with fake tools; no real boot or Yocto parse/build.
