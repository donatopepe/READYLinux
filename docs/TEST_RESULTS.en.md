# Test Results

## 2026-10-18 — Test/status baseline

- Prior WSL systemd security measurement: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Commands: `python -m unittest discover -s tests -v`, `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts, `git diff --check`.
- Verified firing-start snapshot: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json`; HEAD `704a563c7d7a8252e2205304222e7ce0c0dd7384`.
- Historical snapshot `28f5bba753f44fe58ae5063eb93f06f470bec5bd` is retained as context for earlier static tests, not current HEAD.
- Opt-in distro check covers `DISTRO`, `MACHINE` placeholder, systemd init policy and service-recipe autostart.
- Windows/Python 3.11: 96 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 96 tests PASS.
- `compileall`, shell syntax and `git diff --check` pass on both.
- No real BitBake/Yocto parse, build, or QEMU boot.
