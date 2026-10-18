# Test Results

## 2026-10-18 — Evidence history integrity

- IT/EN templates require a unique run ID and append-only records: new record per attempt; corrections use a new record referencing the earlier one.
- Static test checks this policy in both templates.
- `python -m unittest discover -s tests -v` — PASS, 59 tests; compileall, `bash -n`, `git diff --check` — PASS.
- No real build/evidence record created.
