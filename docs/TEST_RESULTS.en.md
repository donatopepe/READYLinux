# Test Results

## 2026-10-18 — Recipe-source guard baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `f9096be2569f10d7bd2d150d8e639ca751475fcf`.
- Historical WSL systemd security finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test guards firing HEAD, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Application recipe `file://` inventory checked statically; no BitBake parse/build or real QEMU boot.
