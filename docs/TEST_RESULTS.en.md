# Test Results

## 2026-10-18 — Yocto path-space baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `d5bb2bab37fdcc99d364d1fc4eed9ce67e928da2`.
- Historical WSL hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression checks firing HEAD, test count and BitBake/QEMU limitations in bilingual status.
- Windows/Python 3.11: 110 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 110 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Validator happy path with space-containing BUILDDIR uses fake BitBake; PASS on WSL, Windows skips POSIX path case. No real parse/build.
