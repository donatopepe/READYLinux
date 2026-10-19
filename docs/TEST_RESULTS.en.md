# Test Results

## 2026-10-18 — Host-preflight/helper baseline

- Partial-host preflight case keeps a valid BUILDDIR but omits required `gcc`; probe must report MISSING and INCOMPLETE.
- Static layer-inventory check pins the recipe set and verifies runtime packages appear in `IMAGE_INSTALL`.
- Static layer inventory pins three `.bb` recipes, forbids unreviewed `.bbappend` files and confirms both runtime packages are listed in `IMAGE_INSTALL`.
- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `e235522d23620db53f91ac86e4b9f205ec24fec2`.
- Historical WSL unit-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test checks firing HEAD, test count and BitBake/QEMU limits in IT/EN status.
- Windows/Python 3.11: 107 tests PASS (5 platform-specific skips); WSL Debian 13/Python 3.13: 107 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positive/negative BUILDDIR and static helpers tested with stubs; no installs/fetches or Yocto parse/build.
