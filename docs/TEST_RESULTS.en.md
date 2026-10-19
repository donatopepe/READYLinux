# Test Results

## 2026-10-18 — Artifact verifier baseline

- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `923e397c3e0d9e7f3b3805731fae95b462f7cc86`.
- Historical WSL unit hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test requires HEAD hash, test baseline and host limitations in both status documents.
- Windows/Python 3.11: 103 tests PASS (2 skips: `systemd-analyze`, unsupported Unix FIFO); WSL Debian 13/Python 3.13: 103 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- FIFO artifact-verifier test PASS on WSL; FIFO identified and rejected without reading; expected skip on Windows.
- No BitBake/Yocto parse/build or real QEMU boot.
