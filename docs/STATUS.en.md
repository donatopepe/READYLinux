# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 100 tests on Windows and WSL (1 `systemd-analyze` skip on Windows); compileall/shell/diff pass. Fake QEMU failure path checks exit propagation and overlay cleanup.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `23a77ce153a5bfcd347a394c26273d7a3dd4d8b3`; QEMU failure-path guard verified, publish pending. `.pi-loop.json` untracked, ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish static audits from parse/runtime.
