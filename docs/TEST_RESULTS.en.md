# Test Results

## 2026-10-18 — Host preflight helper firing baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `e82e9b12b8b3c0d52d99b24cea78fa828b79a1e4`.
- Historical WSL systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to start snapshot; static test guards HEAD hash, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 104 tests PASS (3 platform-specific skips); WSL Debian 13/Python 3.13: 104 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive path tested with command stubs; no installation/fetch and no real BitBake parse/build.
