# Test Results

## 2026-10-18 — QEMU command-line gate baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `630266eab071e744cc8b4bdc5e8f7f1d721cdb6a`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression protects HEAD, test count and bilingual BitBake/QEMU limitations.
- Windows/Python 3.11: 111 tests PASS (7 platform-specific skips); WSL Debian 13/Python 3.13: 111 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- QEMU cmdline negative path uses fake tools and asserts no invocation; no QEMU boot or real Yocto parse/build.
