# Test Results

## 2026-10-18 — Host-preflight/helper baseline

- Missing-BUILDDIR case with all required tools stubbed still reports INCOMPLETE without any MISSING command.
- Partial-host preflight case keeps a valid BUILDDIR but omits required `gcc`; probe must report MISSING and INCOMPLETE.
- Static layer-inventory check pins the recipe set and verifies runtime packages appear in `IMAGE_INSTALL`.
- Static layer inventory pins three `.bb` recipes, forbids unreviewed `.bbappend` files and confirms both runtime packages are listed in `IMAGE_INSTALL`.
- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `5c3c030179abaf1a21225389e98b05b3d0c82bd3`.
- Historical WSL unit-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test checks firing HEAD, test count and BitBake/QEMU limits in IT/EN status.
- Windows/Python 3.11: 108 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 108 tests PASS.
- Latest host-probe evidence: all required command stubs plus valid BUILDDIR passed; absent BUILDDIR with commands present returned INCOMPLETE on WSL.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positive/negative BUILDDIR and static helpers tested with stubs; no installs/fetches or Yocto parse/build.
