# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 97 tests on Windows (1 `systemd-analyze` skip) and WSL; compileall/shell/diff pass. DISTRO/MACHINE opt-in has static contract coverage.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start snapshot `8e0c5277dae03fdbcfc7d772b24d0689f2be1262`; status/test guard refreshed in `3e5fd43`. `.pi-loop.json` local, ZIPs ignored.
- **Next**: parse/build on a release-pinned OE host once selected; keep static audit distinct from metadata parse/runtime evidence.
