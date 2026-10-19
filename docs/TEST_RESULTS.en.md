# Test Results

## 2026-10-18 — Yocto path-space check baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `75f13937c1b5668160059a26c7cb8b222bdb35ba`.
- Historical WSL systemd-security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression checks HEAD, test count and IT/EN BitBake/QEMU limits.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- `validate-yocto-env.sh` happy path with BUILDDIR containing spaces PASS on WSL; BitBake was fake. Windows skips because its temp path is not shared with WSL. No real Yocto parse.
