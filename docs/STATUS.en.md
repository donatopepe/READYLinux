# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 104 tests Windows/Python 3.11 (3 skips: `systemd-analyze`, POSIX FIFO, POSIX PATH-stub probe) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Host-probe positive path tested with stubs.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `e82e9b12b8b3c0d52d99b24cea78fa828b79a1e4`; `.pi-loop.json` and `raw` (0 bytes) untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish stub tests from real build-host evidence.
