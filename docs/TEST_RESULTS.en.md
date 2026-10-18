# Test Results

## 2026-10-18 — Yocto helper preflight

- `python -m unittest tests.test_yocto_validation_script -v` — PASS, 7 tests with fake builddir/bitbake.
- Preflight failures verified: `BUILDDIR`, `bitbake`, `conf/bblayers.conf`, `conf/local.conf`, layer registration.
- Happy path invokes fake `bitbake -p` only after checks pass.
- `python -m unittest discover -s tests -v` — PASS, 50 tests; compileall, `bash -n` on all scripts, and `git diff --check` — PASS.
- No real parse or downloads.
