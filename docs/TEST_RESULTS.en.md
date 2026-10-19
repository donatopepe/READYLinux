# Test Results

## 2026-10-18 — Yocto host-preflight baseline

- Regular-file BUILDDIR regression checks the explicit `Preflight: INCOMPLETE` result.
- Initial snapshot: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `614b1fb8964a992e358b51dd2d0bcf736f5b9a0e`.
- Historical WSL systemd report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test requires HEAD, test baseline and BitBake/QEMU limitations in both status documents.
- Windows/Python 3.11: 105 tests PASS (4 platform-specific skips); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Preflight helper tested with positive/negative stubs; no installation, fetch or real BitBake parse/build.
