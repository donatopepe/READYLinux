# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 81 Windows tests (1 expected systemd-analyze skip) and 81 WSL tests; compileall/shell/diff checks pass. `git check-ignore` confirms both ZIPs ignored.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start snapshot `f8aa2a57ab050cc054dcfd358e6168e6d678a7d3`; ZIP ignore rule added in subsequent commits. `.pi-loop*` excluded.
- **Next**: choose release/BSP and provision BitBake before parse/build. Do not claim reproducibility/boot without README acceptance evidence.
