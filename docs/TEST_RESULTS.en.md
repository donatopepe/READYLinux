# Test Results

## 2026-10-18 — Yocto helper error propagation

- Helper tests: `python -m unittest tests.test_yocto_validation_script -v` — PASS, 9 tests.
- Fake BitBake returns 37; helper propagates exit 37 from `bitbake -p`.
- Full suite `python -m unittest discover -s tests -v` — PASS, 52 tests; compileall, `bash -n` on all scripts, `git diff --check` — PASS.
- Real BitBake unavailable.
