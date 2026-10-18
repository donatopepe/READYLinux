# Test Results

## 2026-10-18 — tty1 ownership

- Documented that `getty@tty1.service` is masked and tty1 reserved for READY.
- Static tests check service, recipe `FILES`, multi-user target, and absence of a competing login service.
- `python -m unittest discover -s tests -v` — PASS, 43 tests; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake/QEMU unavailable; no image or boot verification.
