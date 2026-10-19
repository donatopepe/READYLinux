# Test Results

## 2026-10-18 — Verified baseline at firing start

- README checklist test checks explicit DISTRO/MACHINE, release-series isolation, cached-source caveat and parse/build ordering.
- README test asserts opt-in `DISTRO`, BSP `MACHINE` placeholder, release-series isolation and cache/download caveat precede metadata parse/build commands.
- Start snapshot: `git status --short --branch` showed `main...origin/main` plus untracked `.pi-loop.json`; HEAD `f22e7b969edbe56de9f4412481daf381d8bd4fe6`.
- WSL systemd hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, residual UMask 0027.
- Static test verifies IT/EN status records snapshot, baseline and BitBake/QEMU limitations.
- Windows/Python 3.11: 98 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 98 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` install/validation scripts; `git diff --check`.
- No BitBake/Yocto parse/build, package QA, or real QEMU boot.
