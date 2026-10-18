# Test Results

## 2026-10-18 — Yocto build command sequence

- IT/EN README now show order: `oe-init-build-env` → MACHINE in local.conf → add-layer → parse-only helper → explicit image build.
- Static test checks command order and presence of MACHINE.
- `python -m unittest discover -s tests -v` — PASS, 54 tests; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake unavailable.
