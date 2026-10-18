# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 unit; host preflight, BitBake, systemd, image checksum and isolated/COW QEMU boot helpers.
- **Locally verified**: full 74-test suite rerun pending after QEMU boot helper/README changes; no READY image/kernel exists to boot.
- **Not verified**: BitBake/Yocto parse/build, QEMU image boot, getty mask in image, unit runtime behavior, real READY image artifact, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 logical CPUs, 30 GiB WSL RAM, GCC and QEMU x86_64 installed. BitBake unavailable. No Yocto checkout/fetch performed.
- **Git**: `main` at `7510a11` at start; QEMU COW helper and docs under verification. ZIPs and `.pi-loop*` remain untracked/excluded.
- **Next**: select release/BSP and provide BitBake on Linux before metadata parse/build; do not claim reproducibility/boot until README acceptance evidence exists.
