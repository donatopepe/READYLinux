# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 94 tests on Windows (1 systemd-analyze skip) and WSL; compileall/shell/diff pass. Static test checks bilingual tty/getty contract.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing snapshot `16cea275376886423be22380975094f0cf6d4f45`; tty/getty contract test published in `3afbb81`. ZIPs ignored; `.pi-loop.json` remains local.
- **Next**: parse/build on a release-pinned OE host after selection; do not claim boot/reproducibility without acceptance evidence.
