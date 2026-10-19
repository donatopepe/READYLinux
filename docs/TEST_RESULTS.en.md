# Test Results

## 2026-10-18 — Artifact/QEMU firing baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `2957a95d7d8041992f2ab3c1e9ba71ea044c828a`.
- Historical WSL systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test requires IT/EN status to record snapshot, test baseline and BitBake/QEMU limitations.
- Windows/Python 3.11 suite: 101 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13 suite: 101 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No real BitBake/Yocto parse/build or QEMU boot.
