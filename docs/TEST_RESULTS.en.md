# Test Results

## 2026-10-18 — Yocto runtime dependencies

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 scaffold tests.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- Final full suite: `python -m unittest discover -s tests -v` — PASS, 43 tests.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS; `bash -n install.sh setup-ai-cpu.sh` — PASS; `git diff --check` — PASS.
- `bash -n install.sh setup-ai-cpu.sh` — PASS; scripts unchanged.
- AST scan of runtime modules checks standard-library imports against declared recipe package mapping.
- BitBake unavailable; OE package names/ownership not verified against actual release metadata.
