# Test Results

## 2026-10-18 — systemd state ownership

- Focused static tests: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 tests.
- Verified `StateDirectory`, mode 0750, `UMask`, XDG path, user home/group, and persistent workspace.
- `python -m unittest discover -s tests -v` — PASS, 52 tests; compileall, `bash -n`, and `git diff --check` — PASS.
- No systemd/BitBake runtime validation available.
