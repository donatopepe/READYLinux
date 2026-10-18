# Test Results

## 2026-10-18 — Helper BitBake working directory

- Helper invokes `bitbake -p` from canonical `BUILDDIR`, not caller's cwd.
- Happy-path test uses fake BitBake executable and checks cwd; symlink builddir and preflight branches also covered.
- `python -m unittest discover -s tests -v` — PASS, 51 tests; compileall, `bash -n` on all scripts, and `git diff --check` — PASS.
- Real BitBake unavailable.
