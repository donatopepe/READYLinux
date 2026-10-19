# Test Results

## 2026-10-18 — WSL host-preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `411aa5f09be1c7eb05bf2bae52c0a6b215e0569a`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test protects snapshot HEAD, suite count and BitBake/QEMU limits in the IT/EN status.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- WSL read-only host probe: exit 1 `INCOMPLETE`; 19/19 required commands found, BitBake and BUILDDIR absent; no install/fetch. No Yocto parse/build or QEMU boot.
