# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 98 tests Windows (1 `systemd-analyze` skip) and WSL; compileall/shell/diff pass. License checksum consistency test covers both MIT recipes.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `87d402bd7fe16642117b57f09e70dc0aca867227`; license hash/status audit being refreshed. ZIP ignored; `.pi-loop.json` local.
- **Next**: metadata parse/build on a release-pinned OE host once selected; distinguish static audits from parse/runtime evidence.
