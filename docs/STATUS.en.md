# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 117 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. Offline regressions now cover local sources and image package closure. BitBake/BUILDDIR absent.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; preflight `INCOMPLETE`; no checkout/fetch/install.
- **Git**: firing-start HEAD `0277c37cba956daf6c830fb0d4d8b80cdc81c306`; offline source/package closure tests in `4e49a4e`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned release-pinned OE host; retain reproducible evidence per `docs/VERIFICATION_PLAN.md`.
