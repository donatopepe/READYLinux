# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 111 Windows/Python 3.11 tests (7 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. QEMU cmdline negative-path was tested with fake tools only.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows AMD64 + WSL Debian 13; GCC/QEMU x86_64 present; BitBake unavailable; no Yocto checkout/fetch.
- **Git**: firing-start HEAD `ec5f0817b446e266718661713d6d15965c71a985`; `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when available; distinguish fake-tool tests from real runtime.
