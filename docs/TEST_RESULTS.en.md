# Test Results

## 2026-10-18 — AI/hardware guidance firing baseline

- Initial HEAD: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `4145bd8b748250ac7f3fd0b930389409be3a3e8d`.
- Historical WSL systemd-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Bilingual README and AI hardware docs updated; requested web research not performed: no browser/search tool available and repository rules prohibit network. Tiers remain estimates, not SKU/prices or benchmark results.
- Static status guard protects HEAD and BitBake/QEMU limitations.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check` pass.
- No model/Yocto download, setup or real inference; no Yocto parse/build or QEMU boot.
