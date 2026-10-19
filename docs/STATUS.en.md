# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 108 Windows tests (6 platform-specific skips) and WSL; missing-BUILDDIR probe with all required tools stubbed tested on WSL.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `afd0d88293cb73d83fa219356b5bb54722d90c34`; missing-BUILDDIR preflight test published in `8a5a7a3`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish stubbed evidence from real builds.
