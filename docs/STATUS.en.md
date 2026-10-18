# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened tty1 service; host preflight, BitBake, systemd, artifact checksum, isolated QEMU COW boot helpers.
- **Locally verified**: 76 tests on Windows/MSYS Python 3.11 and WSL Debian 13 Python 3.13; compileall, shell syntax, `git diff --check` pass. systemd unit passes verify; security MEDIUM/6.7 with UMask 0027; fake QEMU checks overlay cleanup/base preservation.
- **Not verified**: BitBake/Yocto parse/build, READY QEMU image boot, getty mask in image, real unit runtime, READY artifact hash, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; QEMU x86_64 and GCC installed; BitBake absent, no Yocto checkout/fetch. Read-only host probe available.
- **Git**: `main` synchronized with `origin/main`; status baseline guard published in `1d4dd26`. ZIPs and `.pi-loop*` remain untracked/excluded.
- **Next**: choose release/BSP and provision BitBake before parse/build; follow README acceptance checklist; no boot/reproducibility claims until evidence exists.
