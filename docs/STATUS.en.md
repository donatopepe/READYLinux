# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 79 tests on Windows/Python 3.11 (1 expected systemd-analyze skip) and WSL/Python 3.13; compileall/shell/diff checks pass. systemd verify/security MEDIUM/6.7, UMask 0027; fake QEMU COW cleanup passes.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start snapshot was `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`; report/status guard updated in commit `218b92b`. ZIPs and `.pi-loop*` excluded.
- **Next**: choose release/BSP and provision BitBake before parse/build. Do not claim reproducibility/boot without README acceptance evidence.
