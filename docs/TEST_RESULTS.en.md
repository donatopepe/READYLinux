# Test Results

## 2026-10-18 — QEMU SSH forwarding baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `4ca49bdd48cbf0ba2f811c2fe1e33d5a951bb855`.
- Historical WSL hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static status regression protects firing HEAD, suite count and BitBake/QEMU limits in both languages.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Fake-QEMU tests verify loopback-only SSH forwarding, networking off by default, and invalid ports rejected before invocation. Guest SSH/real boot/Yocto build not tested.
