# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 79 Windows tests (1 expected skip because `systemd-analyze` is unavailable) and 79 WSL tests; compileall/shell/diff checks pass. systemd unit and fake QEMU COW verified.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: initial snapshot `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`; report alignment published in `16ec02d`, baseline refresh in progress. ZIPs and `.pi-loop*` excluded.
- **Next**: choose release/BSP and provision BitBake before parse/build. Do not claim reproducibility/boot without README acceptance evidence.
