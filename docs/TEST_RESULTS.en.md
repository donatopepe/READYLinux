# Test Results

## 2026-10-18 — Yocto example/schema conformance

- Stdlib test checks nested keys, required fields, SHA/commit patterns, and enums against JSON Schema; no external validator library.
- Focused test — PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 tests; compileall, `bash -n`, `git diff --check` — PASS.
- Example remains explicitly not-built/not-verified.
