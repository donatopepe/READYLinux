# Test Results

## 2026-10-18 — QEMU helper firing baseline

- Full-suite command: `python -m unittest discover -s tests -v`.
- Verified initial HEAD: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json`; `git log -1` = `1a4a348cf180e5c43d3d07eae6071ea23b6e364f`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- New test simulates QEMU exit 23: helper propagates the exit code, removes temporary overlay and preserves the base image.
- Windows/Python 3.11: 100 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 100 tests PASS.
- `compileall`, `bash -n` and `git diff --check` PASS on both.
- BitBake/Yocto metadata parse/build not performed; no real QEMU boot.
