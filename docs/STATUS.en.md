# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 application prototype.
- **Implemented**: Python console, vibe flow, reduced BASIC, Yocto scaffold; tty1 service now runs as dedicated unprivileged `ready` user with persistent state and baseline systemd hardening.
- **Locally verified**: full suite must be rerun after service change; BitBake unavailable.
- **Not verified**: Yocto parse/build/boot/QEMU, OE package mapping, systemd useradd integration, actual tty1/getty, kernel, real GGUF, sandbox, GPU, ARM64, benchmarks.
- **Host**: Windows/MSYS AMD64, Python 3.11; no downloads/installations.
- **Git**: `main` synchronized with `origin/main`; non-root service published in `1e1e8f0`. Exclude ZIPs and `.pi-loop*`.
- **Next**: static hardening/unit checks and full suite, then commit/push; BitBake on Linux host.
- **Risk**: tty1/getty and systemd `StateDirectory` compatibility not tested at boot.
