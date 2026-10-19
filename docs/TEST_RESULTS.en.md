# Test Results

## 2026-10-18 — Yocto recipe baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `bd7b76164f1008657ba9def973fa2736e56ea986`.
- Historical WSL systemd security: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression test protects firing HEAD, suite count and BitBake/QEMU limits.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Application recipe `file://` source guard checked locally. BitBake unavailable: no real parse/build and no downloads.
