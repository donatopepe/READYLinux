# Test Results

## 2026-10-18 — Verified baseline at firing start

- Static SRC_URI extractor now covers URI parameters (`;apply=yes`, `;unpack=0`) and checks the correct local basename; no fetch performed.
- Full-suite command: `python -m unittest discover -s tests -v`.
- Start snapshot: `git status --short --branch` showed `main...origin/main` plus untracked `.pi-loop.json`; HEAD `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`.
- Prior WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to that snapshot; static test guards hash, test baseline and host limitations.
- Windows/Python 3.11: 97 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 97 tests PASS.
- Verified commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts, and `git diff --check` passed on both.
- No real BitBake/Yocto parse/build or QEMU boot.
