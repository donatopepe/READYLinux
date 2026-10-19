# Test Results

## 2026-10-18 — Artifact-to-boot firing baseline

- Initial HEAD: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `0ffc5a57e1ea0d5b04534429340a0a721f3f868b`.
- Historical WSL systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to the firing snapshot; static test guards HEAD hash, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 101 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 101 tests PASS.
- Checks: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No real BitBake/Yocto parse/build or QEMU boot.
