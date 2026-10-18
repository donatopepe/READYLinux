# Test Results

## 2026-10-18 — not-built/not-run state consistency

- Evidence sample checks: not-built images imply null exit/artifact/hash; not-run boot implies all smoke checks not-run.
- Focused Windows test — PASS.
- Windows/Python 3.11 suite — PASS, 59 tests; WSL Debian 13/Python 3.13 suite — PASS, 59 tests.
- Compileall + shell syntax on both — PASS; `git diff --check` — PASS.
- No real parse/build run.
