# Test Results

## 2026-10-18 — Yocto preflight firing baseline

- Initial snapshot: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `afc7962efca1f8c28819e57e340df881ac092299`.
- Historical WSL unit-hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed; static regression checks firing-start HEAD, baseline count and BitBake/QEMU limitations.
- Windows/Python 3.11: 105 tests PASS (4 platform-specific skips); WSL Debian 13/Python 3.13: 105 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive path and invalid BUILDDIR tests use stubs; no install/fetch/real parse-build.
