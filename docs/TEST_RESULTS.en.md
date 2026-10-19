# Test Results

## 2026-10-18 — QEMU helper firing baseline

- Full-suite command: `python -m unittest discover -s tests -v`.
- Verified initial HEAD: `git status --short --branch` = `main...origin/main` plus untracked `.pi-loop.json`; `git log -1` = `286b76eb1654c7fa3a32a0515894aa08ef64ee28`.
- New COW paths-with-spaces test run on Windows/Python 3.11 and WSL Debian 13/Python 3.13: PASS.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Fake QEMU COW tests materialize the overlay and assert it exists during boot; success case covers image/kernel paths with spaces. Success/nonzero exits, cleanup and base-image preservation covered.
- Windows/Python 3.11: 100 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 100 tests PASS.
- `compileall`, `bash -n` and `git diff --check` PASS on both.
- BitBake/Yocto metadata parse/build not performed; no real QEMU boot.
