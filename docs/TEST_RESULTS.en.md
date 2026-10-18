# Test Results

## 2026-10-18 — Evidence sample parse state

- `parse_exit_code` is nullable; `NOT-RUN` sample no longer claims misleading exit 0.
- Test checks `NOT-RUN` log and null exit code.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
- No real parse performed.
