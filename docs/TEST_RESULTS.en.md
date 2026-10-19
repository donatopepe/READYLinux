# Test Results

## 2026-10-18 — Artifact verification → fake boot baseline

- Initial HEAD: `git status --short --branch` showed `main...origin/main` plus untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `ea9ad866c04453ef67ba5b9a8c8e25294917aba4`.
- Historical WSL systemd report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to firing-start HEAD; static test guards snapshot hash, test count and host limits.
- Windows/Python 3.11: 101 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 101 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No Yocto/BitBake parse/build, package QA or real QEMU boot.
