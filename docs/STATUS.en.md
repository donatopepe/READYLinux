# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened non-root systemd tty1 service; BitBake/systemd/image-checksum validation helpers.
- **Locally verified**: 66 tests on Windows/MSYS Python 3.11 and WSL Debian 13 Python 3.13; compileall and `bash -n` on both; `git diff --check` clean. Unit passes WSL `systemd-analyze verify` on a temporary copy with ExecStart substituted. `systemd-analyze security --offline`: MEDIUM, exposure score 6.7, residual UMask 0027.
- **Not verified**: BitBake/Yocto parse/build, QEMU image boot, getty mask in image, unit runtime behavior, real READY image artifact, GGUF, sandbox, GPU/ARM64/benchmarks.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 logical CPUs, 30 GiB WSL RAM, GCC and QEMU x86_64 installed. BitBake unavailable. No Yocto checkout/fetch performed.
- **Git**: `main` synchronized with `origin/main`; baseline refreshed in commit `32cb352`. ZIPs and `.pi-loop*` remain untracked/excluded.
- **Next**: select release/BSP and provide BitBake on Linux before metadata parse/build; do not claim reproducibility/boot until README acceptance evidence exists.
