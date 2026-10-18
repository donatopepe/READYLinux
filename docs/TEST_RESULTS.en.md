# Test Results

## 2026-10-18 — READY BASIC milestone work

- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 37 tests (26 baseline + 11 BASIC).
- `bash -n install.sh setup-ai-cpu.sh` — PASS.
- BASIC tests cover arithmetic, IF/GOTO, FOR/NEXT, INPUT, GOSUB/RETURN, editing, console routing, persistence, malformed input, rejected Python calls/statements, and step-limit enforcement.
- Not covered: Yocto/QEMU boot, real GGUF inference, generated-code sandbox.

## Baseline — 2026-10-18

Windows 10 AMD64, Python 3.11.7. Compileall passed, 26 unit/integration tests passed, shell syntax checks passed. HTTP AI tests use mocks; real model inference is untested.
