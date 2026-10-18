# READY Linux Baseline

Recorded: 2026-10-18. Source baseline: `READYLinux_0.3_Codex_Handoff.zip`, extracted at repository root.

## Verified product state

- READY 0.3 is a Python terminal application, not a Linux distribution or desktop.
- Numbered programming is implemented in Python; there is no Commodore BASIC parser/runtime in the baseline.
- Optional local-AI workflow proposes JSON file changes with diff, approval, static checks, and explicit execution.
- `vibe.py` manages workspaces/proposals; `ai_local.py` calls local llama-server.
- Real GGUF inference, a verified sandbox, bootable image, and GUI are not implemented or verified.

## Verification environment

- Host: Windows 10, AMD64; Python 3.11.7; Python reports 20 logical processors.
- Available: Git 2.49.0, Node, Pi CLI.
- Not found in PATH: BitBake, QEMU x86-64/ARM64, Docker/Podman, Clang, GCC.
- RAM not measured (`free` unavailable in MSYS environment).

## Baseline tests

- `python -m compileall -q readylinux.py ai_local.py vibe.py`: pass.
- `python -m unittest discover -s tests -v`: 26 tests pass.
- `bash -n install.sh setup-ai-cpu.sh`: pass.
- AI HTTP tests use a mock server; no real inference was tested.

## Repository

Git root is READY Linux repository; branch `main`, remote `https://github.com/donatopepe/READYLinux.git`. No commits yet. ZIP archives are local source inputs, not runtime dependencies.
