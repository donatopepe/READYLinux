# Test Results

## 2026-10-18 — WSL toolchain available

- `wsl -d Debian -- ...`: Debian GNU/Linux 13 trixie, x86_64; 20 logical CPUs, 30 GiB RAM.
- Installed in WSL at user request: build tools (`gcc`, `make`, Python/deps) and QEMU x86_64; no Yocto/BitBake checkout or build-source fetch performed yet.
- QEMU available; BitBake absent. No image build started.
- Unit suite passes on both Windows and WSL after path-portability fixes: 59 tests each. Full commands are listed below.

## 2026-10-18 — Cross-platform Yocto helper tests

- Windows/Python 3.11: `python -m unittest discover -s tests -v` — PASS, 59 tests.
- WSL Debian 13/Python 3.13: same command — PASS, 59 tests.
- `compileall` and `bash -n` on Windows and WSL — PASS. Fake BitBake layer paths generated using canonical WSL paths.
- BitBake itself remains unavailable.

## 2026-10-18 — Evidence artifact integrity

- Static tests `python -m unittest tests.test_yocto_scaffold -v` — PASS, 13 tests.
- Guides/templates require `sha256sum <artifact>`, image/log retention paths, and prohibit committing binaries/credentials.
- No image artifact is available to hash.
