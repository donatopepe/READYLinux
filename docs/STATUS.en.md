# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 111 tests Windows (7 platform-specific skips) and WSL; QEMU helper rejects an empty kernel cmdline before tools. No real boot.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`; empty-kernel-cmdline QEMU guard published in `93c17dc`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a Linux OE host with pinned release when available; distinguish fake BitBake from real parse/build.
