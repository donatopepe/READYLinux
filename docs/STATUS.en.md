# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 114 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; compileall/shell/diff pass. WSL host preflight exits 1 for missing BitBake/BUILDDIR; fake local checks are distinct from real gates.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH service, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; probe found 19/19 required commands but no `bitbake`/`bitbake-layers` and no `BUILDDIR`. No checkout/install/fetch.
- **Git**: firing-start HEAD `eee12774e2408514a6839eaa286de25890fdf4f0`; `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned release-pinned OE host; follow `docs/VERIFICATION_PLAN.md` and retain real output/logs.
