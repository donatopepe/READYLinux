# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 97 Windows tests (1 `systemd-analyze` skip) and WSL tests; compileall/shell/diff pass. Static checks link stdlib RDEPENDS and image packages.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`; dependency-closure guard published in `764c9b4`. ZIP ignored; `.pi-loop.json` local.
- **Next**: metadata parse/build on a release-pinned OE host once selected; distinguish static audits from parse/runtime evidence.
