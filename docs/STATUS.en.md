# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 103 Windows/Python 3.11 tests (2 skips: `systemd-analyze`, POSIX FIFO) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Artifact verifier FIFO guard has local coverage.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `dbad747059f7fce6304ad2c267d8ce6444572ceb`; `.pi-loop.json` and `raw` (0 bytes) untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish helper tests from parse/build/hardware evidence.
