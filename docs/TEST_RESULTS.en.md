# Test Results

## 2026-10-18 — Yocto install-path ownership

- Suite command: `python -m unittest discover -s tests -v`; compileall and shell syntax are also part of cross-host run.
- Suite command: `python -m unittest discover -s tests -v`; `python -m compileall`; `bash -n` static shell checks are part of the full run.
- Static test verifies every runtime/service/getty-mask path from `do_install` is covered by matching recipe `FILES:${PN}`.
- Also checks getty-mask symlink and matching `SYSTEMD_SERVICE` declaration.
- Windows/Python 3.11 suite — PASS, 86 tests (1 systemd-analyze skip); WSL Debian 13/Python 3.13 suite — PASS, 86 tests.
- Test does not replace BitBake/package QA. QEMU boot not run.
- Compileall, shell syntax on both, `git diff --check` — PASS.
- Prior systemd finding: `systemd-analyze security --offline`, `MEDIUM/6.7`, UMask 0027.
