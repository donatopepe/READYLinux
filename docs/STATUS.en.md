# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 82 Windows tests (1 expected systemd-analyze skip) and 82 WSL tests; compileall/shell/diff checks pass. ZIP ignore and layer override syntax statically checked.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing snapshot `f8aa2a57ab050cc054dcfd358e6168e6d678a7d3`; override/ignore tests published in `0794736`. ZIPs excluded; `.pi-loop.json` untracked.
- **Next**: choose release/BSP and provision BitBake before parse/build. Do not claim reproducibility/boot without README acceptance evidence.
