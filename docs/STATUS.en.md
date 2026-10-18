# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: Python console, vibe flow, reduced BASIC, Yocto layer and non-root tty1 systemd service with persistent state, hardening, and tty1 getty masked.
- **Locally verified**: 43 tests, compileall, `bash -n`, `git diff --check`; static tests cover tty1 ownership and deferred-serial constraint. BitBake/QEMU unavailable.
- **Not verified**: Yocto parse/build/boot/QEMU, actual getty mask, login/console boot, OE package mapping, kernel, real GGUF, sandbox, GPU, ARM64, benchmarks.
- **UX impact**: tty1 is reserved for READY; no normal login prompt on that terminal. Serial console is deferred until BSP/target is selected.
- **Host**: Windows/MSYS AMD64, Python 3.11; no downloads/installations.
- **Git**: `main` at `21b20e6` at firing start; console target-selection docs verified, publication in progress. Exclude ZIP/loop state.
- **Next**: select Yocto release + machine/BSP before adding serial console; continue local M2 checks meanwhile. BitBake remains unverified on Linux host.
