# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 101 tests Windows (1 `systemd-analyze` skip) and WSL; compileall/shell/diff pass. Fake QEMU overlay lifecycle and spaced paths covered.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `286b76eb1654c7fa3a32a0515894aa08ef64ee28`; QEMU paths-with-spaces regression published in `d7a817d`. `.pi-loop.json` and `raw` (0-byte) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish simulated tests from real build/hardware evidence.
