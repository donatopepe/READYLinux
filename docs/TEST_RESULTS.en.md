# Test Results

## 2026-10-18 — Artifact verifier baseline

- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `dbad747059f7fce6304ad2c267d8ce6444572ceb`.
- Historical WSL unit-hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN snapshot guard verifies HEAD, test baseline and BitBake/QEMU limitations.
- Windows/Python 3.11: 103 tests PASS (2 skips: `systemd-analyze`, unsupported Unix FIFO); WSL Debian 13/Python 3.13: 103 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier rejects Unix FIFO without blocking; expected skip on Windows. No Yocto parse/build or real QEMU boot.
