# Test Results

## 2026-10-18 — Artifact verifier checks

- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw`; `git log -1` = `71610716030e5a02cbb2ad0839b946cba1387f89`.
- Previous WSL `systemd-analyze security --offline` finding: MEDIUM/6.7, UMask 0027.
- Static test verifies status snapshot, test baseline and host limits in IT/EN docs.
- Windows/Python 3.11: 103 tests PASS (2 skips: `systemd-analyze`, unsupported Unix FIFO); WSL Debian 13/Python 3.13: 103 tests PASS.
- `compileall`, `python -m unittest discover -s tests -v`, `bash -n` scripts and `git diff --check` run.
- FIFO test confirms `is_fifo()`, nonblocking verifier rejection, and no FIFO read.
- No BitBake/Yocto parse/build or real QEMU boot.
