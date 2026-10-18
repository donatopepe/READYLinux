# Test Results

## 2026-10-18 — Yocto launcher

- Fixed installed launcher: quoted heredoc does not expand BitBake variables; runtime path is now static `/usr/share/readylinux/readylinux.py`.
- Focused test: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 tests.
- Final full suite: `python -m unittest discover -s tests -v` — PASS, 43 tests; `compileall`, `bash -n`, and `git diff --check` — PASS.
- BitBake unavailable; package/image not built.
