# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 97 tests Windows/Python 3.11 (1 `systemd-analyze` skip) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Static SRC_URI parsing covers `;apply`/`;unpack` options.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing snapshot `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`; SRC_URI option test and baseline updated in this firing. ZIPs ignored; `.pi-loop.json` local.
- **Next**: metadata parse/build on a release-pinned OE host once selected; distinguish static audits from parse/runtime evidence.
