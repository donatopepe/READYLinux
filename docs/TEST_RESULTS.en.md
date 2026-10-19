# Test Results

## 2026-10-18 — Host preflight helper firing baseline

- Negative preflight test passes a regular file as BUILDDIR and verifies it is reported unset/incomplete.
- QEMU SHA-mismatch guard asserts qemu tools are not invoked and rejected base-image bytes remain unchanged.
- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `35f6506d310678b2387c542bef0c492a10e3e5c8`.
- Historical WSL systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to start snapshot; static test guards HEAD hash, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 105 tests PASS (4 platform-specific skips); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive path tested with command stubs; no installation/fetch and no real BitBake parse/build.
