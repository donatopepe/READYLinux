# Test Results

## 2026-10-18 — Host-preflight snapshot baseline

- Bilingual hardware buying guidance added as dated capacity tiers/verification policy; live web research deferred (no browser tool available; repository rules prohibit network access). Treat values as estimates, not tested requirements.
- Static Yocto recipe contract verifies inventory, shared MIT/checksum metadata and runtime dependencies for application/console packages.
- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `704cdb5e452dba805816e0f865232a28faeb2294`.
- Previous WSL systemd-hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression requires HEAD, suite count and BitBake/QEMU limits in IT/EN status.
- Prior WSL unit-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host-probe positive/negative BUILDDIR cases tested with stubs; no install/fetch/real parse/build. No web research or hardware/model download was performed.
