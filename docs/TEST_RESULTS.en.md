# Test Results

## 2026-10-18 — Evidence sample privacy

- Static test rejects password, token, and private-key markers in example JSON.
- IT/EN guides state example is placeholder-only and credentials must be redacted before storing real evidence.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
