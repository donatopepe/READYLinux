# Test Results

## 2026-10-18 — tty1 exclusivity

- Console recipe installs `/etc/systemd/system/getty@tty1.service -> /dev/null` because READY owns tty1.
- Focused `python -m unittest tests.test_yocto_scaffold -v` — PASS before full verification.
- `python -m unittest discover -s tests -v` — PASS, 43 tests; compileall, `bash -n`, and `git diff --check` — PASS.
- BitBake/QEMU unavailable: no real getty mask or boot verification.
