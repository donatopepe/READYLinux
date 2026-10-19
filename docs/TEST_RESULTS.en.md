# Test Results

## 2026-10-18 — Firing baseline and static audit

- Full-suite command: `python -m unittest discover -s tests -v`.
- Initial HEAD: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json`; `git log -1` = `81298d7dc97c40ab96ac39725d9a0b720b086320`.
- IT/EN status refreshed to this snapshot; static test guards hash, baseline and host limitations.
- Windows/Python 3.11: 98 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 98 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` scripts; `git diff --check` pass on both.
- Historical WSL systemd security measurement: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- No real BitBake/Yocto parse/build or QEMU boot; BitBake and a release-pinned checkout are absent.
