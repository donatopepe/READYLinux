# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 174 Windows/Python 3.11 tests (8 platform-specific skips) and WSL Debian 13/Python 3.13; suite, compileall and shell syntax pass. Preflight run inside WSL Debian 13: 19/19 required host commands `OK`, `qemu-system-x86_64` found, `bitbake`/`bitbake-layers` absent, `BUILDDIR` unset; exit 1 `INCOMPLETE`. The probe launched from the Windows shell is not a valid Debian host and is not used as evidence.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; preflight `INCOMPLETE`; no checkout/fetch/install.
- **Git**: firing-start HEAD `cc7c8ccf4363022dba5e009d68178cffe8ea8a06`; package-override syntax/uniqueness guard in `2c3452a`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned release-pinned OE host; only update the evidence record after a real parse.
