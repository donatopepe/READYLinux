# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/reduced BASIC, Yocto scaffold, non-root tty1 systemd service; BitBake preflight, systemd syntax, and image SHA-256 verifier helpers.
- **Locally verified**: 66 tests pass on Windows and WSL; compileall/shell syntax on both; unit verified on WSL; image checksum helper tested with fixtures.
- **Not verified**: BitBake/Yocto parse/build, QEMU image boot, checksum for a real READY image, getty mask inside image, full runtime policy, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13, 20 logical CPUs, about 30 GiB WSL RAM; GCC/QEMU x86_64 installed. BitBake absent; no Yocto checkout/download performed.
- **Git**: `main` synced with `origin/main`; image checksum helper under verification. Exclude ZIPs and `.pi-loop*`.
- **Next**: publish after Windows/WSL tests; BitBake/OE setup remains required for real parse/build; no Yocto checkout selected.
