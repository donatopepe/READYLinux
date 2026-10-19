# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 99 tests Windows (1 `systemd-analyze` skip) and WSL; compileall/shell/diff pass. README clean-build checklist and recipe ownership statically checked.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable, no Yocto checkout/fetch.
- **Git**: firing-start HEAD `7fbe08e17072d45c070c847b14825097228f3dfe`; checklist guard published in `ad49c7c`. `.pi-loop.json` untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host once selected; keep static audit distinct from parse/runtime.
