# Test Results

## 2026-10-18 — Hardware guidance documentation baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `e07025bf1b89ca7e6926dae78a0db884100a143f`.
- Historical WSL systemd hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status test checks firing HEAD, test count and BitBake/QEMU limitations.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- README/docs link the bilingual capacity-estimate hardware guide; no web research/download/real inference was performed. No Yocto parse/build or QEMU boot.
