# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: suite/QEMU fake-tool evidence is listed in `TEST_RESULTS.en.md`; opt-in SSH bridge awaits a bootable image/guest server; no SSH boot has been verified.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH service, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; read-only host preflight exit 1 `INCOMPLETE`: 19/19 required commands OK, QEMU+sha256sum present, BitBake/bitbake-layers absent, BUILDDIR unset; no package changes. No checkout/fetch/install started.
- **Git**: firing-start HEAD `4ecf470a867f391f22c5f257c661df6a229242f3`; verification plan refreshed in `b62cf95`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: metadata parse/build on a release-pinned OE host when available; distinguish fake argument tests from real boot/guest SSH.
