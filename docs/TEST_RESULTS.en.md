# Test Results

## 2026-10-18 — Yocto validator path-space baseline

- Firing start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `d03fc9cb9a830912363c30d20514cba83f7c9a0f`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status guard protects snapshot/HEAD and BitBake/QEMU limits.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Spaced-BUILDDIR validator happy path invokes only fake BitBake on WSL; Windows skips because temp path not shared. No real parse/build.
