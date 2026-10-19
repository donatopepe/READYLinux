# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 114 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Read-only WSL preflight: 19/19 host commands present, BitBake and BUILDDIR absent.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; host probe `INCOMPLETE`; no fetch/install/checkout.
- **Git**: firing-start HEAD `d3b21733de5299dae53fcf4c75e021481ff7883b`; WSL preflight baseline guard in `b55d846`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A metadata parse on an already provisioned release-pinned OE host; retain exact logs and versions.
