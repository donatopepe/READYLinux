# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 110 Windows/Python 3.11 tests (7 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Yocto env validator with spaced `BUILDDIR` tested on WSL using fake BitBake.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `d03fc9cb9a830912363c30d20514cba83f7c9a0f`; current firing snapshot guard in `a052e87`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a Linux OE host with pinned release when available; distinguish fake BitBake from real parse/build.
