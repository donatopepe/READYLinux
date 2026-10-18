# Test Results

## 2026-10-18 — Local systemd unit validation

- WSL Debian 13/systemd 257 `systemd-analyze verify` — PASS using a temporary copy with ExecStart substituted; tracked unit untouched.
- Helper missing-systemd-analyze test now passes on Windows/MSYS and WSL.
- Updated suite: 62 tests on Windows/Python 3.11 and 62 on WSL/Python 3.13 — PASS.
- `compileall` and `bash -n` on both — PASS; `git diff --check` — PASS.

- `bash scripts/validate-systemd-unit.sh` on WSL Debian 13/systemd 257 — PASS; no warning/error.
- Script substitutes `ExecStart` with `/bin/true` only in a temporary copy; tracked source is unchanged. This is not image integration/boot validation.
- `python -m unittest tests.test_systemd_validation_script -v` — PASS, 3 tests.
- Windows/Python 3.11 suite — PASS, 62 tests; WSL Debian 13/Python 3.13 suite — PASS, 62 tests.
- Compileall and shell syntax on both — PASS; `git diff --check` — PASS.
