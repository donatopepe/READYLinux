# Test Results

## 2026-10-18 — Yocto validator path spaces

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `1ab9e0ce3dbec67cb9b7a201f254e55c5945cbec`.
- Historical WSL hardening assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test protects firing HEAD, suite count, and BitBake/QEMU limits in IT/EN status.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Yocto validator with BUILDDIR containing spaces PASS on WSL using fake BitBake; Windows skips because temp path is outside WSL filesystem. No real parse.
