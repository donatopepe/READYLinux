# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 103 tests Windows (2 platform-specific skips) and WSL; artifact verifier rejects non-image directories and Unix FIFOs.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `c8ec19a0425d2566cd74fc19e44c379f0a0d9cc2`; non-regular image-input guard in `78dd021`. `.pi-loop.json` and `raw` (0 bytes) untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish helper tests from real build/hardware evidence.
