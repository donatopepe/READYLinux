# Test Results

## 2026-10-18 — M2 Yocto scaffold

- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 42 tests.
- `bash -n install.sh setup-ai-cpu.sh` — PASS.
- Static scaffold checks validate layer metadata, local recipe sources, image dependency, enabled systemd tty1 unit, and no external fetch URI.
- BitBake is unavailable in the Windows/MSYS environment; no BitBake parse, image build, or QEMU boot was run.

## Baseline / BASIC

Windows 10 AMD64, Python 3.11.7. Earlier baseline 26 tests; BASIC implementation suite 37 tests. Mocked HTTP tests are not real GGUF inference.
