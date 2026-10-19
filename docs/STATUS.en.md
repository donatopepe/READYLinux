# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 109 Windows/Python 3.11 tests (6 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Hardware guidance is capacity-based estimate, not current market research.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `4145bd8b748250ac7f3fd0b930389409be3a3e8d`; bilingual hardware guidance updated in `39cf91f`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish estimates from verified hardware recommendations.
