# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 114 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. WSL read-only host probe found all required commands but BitBake/bitbake-layers and BUILDDIR are unavailable.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; 19/19 required commands OK, QEMU available; BitBake/bitbake-layers absent, BUILDDIR unset. No fetch/install.
- **Git**: firing-start HEAD `75b12e66324b51a9631754b63b03a17ebe3f0300`; WSL preflight baseline guard in `0df6b70`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned, release-pinned OE host; retain full command output per `docs/VERIFICATION_PLAN.md`.
