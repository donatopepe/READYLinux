# Test Results

## 2026-10-18 — Artifact helper baseline

- Initial snapshot: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `c8ec19a0425d2566cd74fc19e44c379f0a0d9cc2`.
- Historical WSL systemd hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test requires HEAD, baseline and host limits in IT/EN status.
- Windows/Python 3.11: 103 tests PASS (2 skips: `systemd-analyze`, POSIX FIFO); WSL Debian 13/Python 3.13: 103 tests PASS.
- Verifier input audit covers missing/empty files and a non-empty directory bearing an image suffix; the directory is rejected.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No BitBake/Yocto parse/build or real QEMU boot.
