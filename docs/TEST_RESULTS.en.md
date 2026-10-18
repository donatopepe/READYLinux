# Test Results

## 2026-10-18 — Console target selection

- Documented decision: generic scaffold uses tty1; serial console deferred until a BSP/machine is selected because device names and login policy vary by target.
- Static test checks this constraint.
- `python -m unittest discover -s tests -v` — PASS, 43 tests; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake/QEMU unavailable.
