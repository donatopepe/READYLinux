# READY Linux Status

Updated: 2026-10-18.

- **Release**: READY Linux 0.3 prototype.
- **Implemented**: console, vibe/BASIC, Yocto scaffold, hardened non-root tty1 service; BitBake/systemd/image SHA validation helpers.
- **Verified**: 66 tests pass on Windows and WSL; WSL systemd-analyze verify PASS; systemd security reports MEDIUM exposure (UMask 0027, group-readable files). Hardening assertions updated.
- **Not verified**: BitBake/image build, QEMU boot, getty mask in image, target service runtime, model/sandbox/GPU/ARM64.
- **Host**: Windows + WSL Debian 13, QEMU x86_64 installed; BitBake absent. No Yocto sources checked out.
- **Git**: `main` was at `e102b32`; systemd unit verified locally, publish in progress. Exclude ZIPs and `.pi-loop*`.
- **Next**: cross-platform tests, record security exposure metric, publish.
