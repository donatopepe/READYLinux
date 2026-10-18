# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 91 tests on Windows (1 systemd-analyze skip) and WSL; compileall/shell/diff pass. Writable paths statically scoped to persistent state; README/unit hardening consistent.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present, BitBake absent; no Yocto checkout/fetch.
- **Git**: firing-start snapshot `0af873121688d50fd187afb01f3bd671d4be2ab7`; writable-state guard published in `a547aef`. ZIPs ignored; `.pi-loop.json` remains local.
- **Next**: parse/build on a release-pinned OE host after selection; do not claim boot/reproducibility without acceptance evidence.
