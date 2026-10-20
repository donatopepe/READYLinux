# READY Linux Status

Updated: 2026-10-18.

Note: local ZIP archives are ignored by Git (`*.zip`) and may remain untracked.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 188 Windows/Python 3.11 tests (14 platform-specific skips) and WSL Debian 13/Python 3.13; suite, compileall and shell syntax pass. Preflight run inside WSL Debian 13: 19/19 required host commands `OK`, `qemu-system-x86_64` found, `bitbake`/`bitbake-layers` absent, `BUILDDIR` unset; exit 1 `INCOMPLETE`. The probe launched from the Windows shell now exits 2 `NOT-A-LINUX-HOST` (`WRONG-ENVIRONMENT`) and is not used as evidence (0 = ready, 1 = `INCOMPLETE`, 2 = wrong environment). `--json` emits a machine-readable report with `verdict` `ready`/`incomplete`/`not-a-linux-host`, command map and `builddir`; unknown arguments exit 64. `scripts/record-yocto-preflight.py OUT.json` records the report with commit and UTC, refuses to write unless the preflight is `ready` (exit 3) and will not overwrite without `--force` (exit 4). Schema `docs/YOCTO_PREFLIGHT_RECORD.schema.json` (draft 2020-12) validates the record; `docs/YOCTO_PREFLIGHT_RECORD.example.json` is placeholder-only.
- **Not verified**: real BitBake/Yocto parse/build, READY QEMU image boot, guest SSH, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPUs; preflight `INCOMPLETE`; no checkout/fetch/install.
- **Git**: firing-start HEAD `cc7c8ccf4363022dba5e009d68178cffe8ea8a06`; package-override syntax/uniqueness guard in `2c3452a`. `.pi-loop.json` and `raw` (0 bytes) untracked; ZIPs ignored.
- **Next**: Gate A parse on an already provisioned release-pinned OE host; only update the evidence record after a real parse.
