# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 114 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Read-only WSL preflight found 19/19 required commands, but BitBake/BUILDDIR are absent.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; preflight INCOMPLETE; no fetch/install/checkout.
- **Git**: firing-start HEAD `2fa33faaa4311927fdbd788ede95f36d6e74a656`; `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: parse/build gates on an already provisioned release-pinned OE host; retain logs and versions in evidence record.
