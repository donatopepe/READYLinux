# Test Results

## 2026-10-18 — Yocto install-path ownership

- Suite command: `python -m unittest discover -s tests -v`; `python -m compileall`; `bash -n` static shell checks are part of the full run.
- Static test verifies every runtime/service/getty-mask path from `do_install` is covered by matching recipe `FILES:${PN}`.
- Also checks getty-mask symlink and matching `SYSTEMD_SERVICE` declaration.
- Focused Windows/Python 3.11 and WSL Debian 13/Python 3.13 test — PASS.
- Does not replace BitBake/package QA; full suite rerun pending. QEMU boot not run.
- Prior systemd finding: `systemd-analyze security --offline`, `MEDIUM/6.7`, UMask 0027.
