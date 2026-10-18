# Test Results

## 2026-10-18 — BASIC runtime M1 (in progress)

- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 37 tests (26 baseline + 11 BASIC).
- `bash -n install.sh setup-ai-cpu.sh` — PASS.
- BASIC coverage: output/arithmetic, IF/GOTO, FOR/NEXT, INPUT, GOSUB/RETURN, edit/delete/list, console save/load, rejection of Python calls and unknown statements, execution step limit.
- This does not verify full Commodore BASIC compatibility, generated-code sandboxing, or embedded OS.

## Baseline — 2026-10-18

Windows 10 AMD64, Python 3.11.7. Compileall passed, 26 unit/integration tests passed, shell syntax checks passed. HTTP AI tests use mocks; real model inference is untested.
