# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 98 Windows/Python 3.11 tests (1 `systemd-analyze` skip) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Static recipe license/dependency/SRC_URI audits.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable, no Yocto checkout/fetch.
- **Git**: firing-start HEAD `d9c8f9ab6d9832741a38c29f34dac2a3e2d80318`; baseline/license guard in progress. `.pi-loop.json` untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host once selected; distinguish static audits from parse/runtime evidence.
