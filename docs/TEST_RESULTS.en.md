# Test Results

## 2026-10-18 — Yocto host probe

- Full suite command: `python -m unittest discover -s tests -v`.
- Initial snapshot: `git status --short --branch` showed `main...origin/main` and untracked `.pi-loop.json`/`raw`; HEAD `088d7f42bcc37fba1f1d8edca5a68332c757a888`.
- Historical WSL systemd hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test guards snapshot and test-count reporting in both status docs.
- Windows/Python 3.11: 104 tests PASS (3 skips: `systemd-analyze`, POSIX FIFO, POSIX PATH-stub probe); WSL Debian 13/Python 3.13: 104 tests PASS.
- Full suites plus `compileall`, `bash -n`, `git diff --check` run on both.
- Host probe success/failure tested with command stubs; BitBake and QEMU unavailable. No install, fetch or real Yocto build.
