# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 101 tests Windows (1 `systemd-analyze` skip) and WSL; compileall/shell/diff pass. Artifact verification to fake QEMU with spaced paths covered.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `752a2578cacd309202a36957907634ea6cfb01cd`; artifact-to-fake-boot integration test published in `60a49ab`. `.pi-loop.json` and `raw` (0-byte) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when selected; distinguish simulated tests from real build/hardware evidence.
