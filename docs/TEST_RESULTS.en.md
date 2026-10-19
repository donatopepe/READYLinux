# Test Results

## 2026-10-18 — Hardware guidance status baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `1aaa8c5b882ae04e3d1f70c1be32731b47191e25`.
- Historical WSL systemd-security check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard checks HEAD/hash, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- IT/EN hardware guide labels guidance as capacity-based estimate; no web research/download. BitBake/Yocto and QEMU build/boot unavailable.
