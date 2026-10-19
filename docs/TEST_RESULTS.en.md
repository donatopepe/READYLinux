# Test Results

## 2026-10-18 — Test/status baseline

- Commands: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` scripts; `git diff --check`.
- Verified firing-start snapshot: `git status --short --branch` showed `main...origin/main`; HEAD `8e0c5277dae03fdbcfc7d772b24d0689f2be1262`, `.pi-loop.json` untracked.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status cites the firing-start snapshot; static test guards snapshot, test count and BitBake/QEMU limits.
- Verified baseline: 97 Windows/Python 3.11 tests (1 `systemd-analyze` skip) and 97 WSL Debian 13/Python 3.13 tests.
- `compileall`, shell syntax and `git diff --check` pass on both.
- No Yocto parse/build, package QA or real QEMU boot.
