# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 96 tests Windows (1 systemd-analyze skip) and WSL; compileall/shell/diff pass. Distro systemd/init policy matches service recipe and README.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing snapshot `28f5bba753f44fe58ae5063eb93f06f470bec5bd`; distro systemd contract test published in `7283fb6`. ZIPs ignored; `.pi-loop.json` remains local.
- **Next**: parse/build on a release-pinned OE host after selection; do not claim boot/reproducibility without acceptance evidence.
