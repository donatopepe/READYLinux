# Test Results

## 2026-10-18 — Yocto service security regressions

- Added static assertions for unprivileged identity, required hardening, write-path restriction, and absence of capability/privilege overrides.
- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 tests; full suite — PASS, 52 tests.
- `compileall`, `bash -n` on all scripts, `git diff --check` — PASS.
- BitBake/systemd unavailable for metadata/runtime validation.
