# Test Results

## 2026-10-18 — Image excludes AI weights

- Static tests verify image recipe has no `SRC_URI`, URL, GGUF model, or llama runtime; runtime recipe accepts local software sources only.
- Docs clarify AI weights/runtime are excluded and provisioning is explicit.
- `python -m unittest discover -s tests -v` — PASS, 52 tests; compileall, `bash -n`, and `git diff --check` — PASS.
- BitBake unavailable: built image contents not verified.
