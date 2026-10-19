# Test Results

## 2026-10-18 — Hardware guidance firing baseline

- Initial snapshot: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `5ef5181285cb64446d660452c89538f8aa82e462`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status updated; static guard checks HEAD, test count, and BitBake/QEMU limits.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Hardware guidance remains bilingual and marked estimate; web research not performed because no browser tool is available and network is prohibited. No model download/inference, Yocto build, or QEMU boot.
