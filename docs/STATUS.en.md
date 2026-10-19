# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 114 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Read-only WSL preflight found BitBake/bitbake-layers and BUILDDIR absent; detail is in verification plan.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH service, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; 19/19 required host commands found; BitBake/bitbake-layers absent; BUILDDIR unset. No package changes/fetch/install.
- **Git**: firing-start HEAD `ffe6d5b6563c42baaecac7de738767cc2b6089f5`; WSL preflight baseline guard in `f49de76`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned, release-pinned OE host; retain complete output in a build evidence record.
