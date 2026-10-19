# Test Results

## 2026-10-18 — Hardware documentation baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `4a3c4da1e8339070f7a388247340c810bed87332`.
- Prior WSL hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static guard checks reported snapshot and documented test/BitBake/QEMU limits.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Hardware recommendation policy updated without web research (no browser/search tool; network prohibited). Capacity estimates only, not benchmarked requirements or verified SKUs.
- No model download, real inference, Yocto build or QEMU boot.
