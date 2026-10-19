# Test Results

## 2026-10-18 — Artifact verification firing baseline

- Initial HEAD: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json` and `raw`; `git log -1` = `8460bab096e72defa1301253dedbaaa8a3f09b08`.
- Historical WSL unit-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status records snapshot, test count and Yocto limitations; static test guards those fields.
- Windows/Python 3.11 suite: 101 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 101 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Local artifact verifier covers valid/invalid checksum, invalid input, symlink and spaced path without mutation. Fake QEMU integration remains separate.
- No real BitBake/Yocto parse/build, package QA or QEMU boot.
