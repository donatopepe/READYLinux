# Test Results

## 2026-10-18 — Status baseline consistency

- IT/EN status aligned to HEAD `c6d98eda388edb1085c74c8812a4484ae26399cf`, test count 75, Windows/WSL, BitBake/boot limits, and systemd MEDIUM/UMask finding.
- Added static test for cited commit, host limits, absence of build claim, and UMask in both status files.
- Windows/Python 3.11 suite — PASS, 77 tests (1 expected skip: systemd-analyze unavailable); WSL Debian 13/Python 3.13 suite — 77 tests.
- Compileall and shell syntax on both — PASS; `git diff --check` — PASS.
