# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened non-root tty1 service; read-only host prerequisite probe, BitBake preflight, systemd and image checksum helpers.
- **Locally verified**: 70 tests on Windows/WSL; compileall, shell syntax and diff check pass. WSL probe finds 19/19 host commands, QEMU and package versions; BitBake/BUILDDIR absent.
- **Not verified**: BitBake/Yocto parse/build, QEMU image boot, getty mask in image, unit runtime behavior, real READY image artifact, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 logical CPUs, 30 GiB WSL RAM, GCC and QEMU x86_64 installed. BitBake unavailable. No Yocto checkout/fetch performed.
- **Git**: `main` was at `4121596`; host probe tested, publish in progress. ZIPs and `.pi-loop*` remain untracked/excluded.
- **Next**: select release/BSP and provide BitBake on Linux before metadata parse/build; do not claim reproducibility/boot until README acceptance evidence exists.
