# Test Results

## 2026-10-18 — QEMU helper firing baseline

- Full-suite command: `python -m unittest discover -s tests -v`.
- Verified initial HEAD: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json`; `git log -1` = `05c60562680e6b5b9ef8d371beff878a82c0ad39`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Fake QEMU COW tests materialize the overlay; fake QEMU checks it exists during boot. Success/nonzero exits, cleanup and base-image preservation covered.
- Windows/Python 3.11: 100 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 100 tests PASS.
- `compileall`, `bash -n` and `git diff --check` PASS on both.
- BitBake/Yocto metadata parse/build not performed; no real QEMU boot.
