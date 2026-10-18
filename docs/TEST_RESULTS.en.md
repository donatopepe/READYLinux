# Test Results

## 2026-10-18 — Read-only Yocto prerequisites probe

- `scripts/check-yocto-host.sh` reports distro/arch/CPU, required host commands, key package versions, BitBake/QEMU and BUILDDIR; no install/download.
- Focused `python -m unittest tests.test_yocto_host_check -v` — PASS, 4 tests on Windows and WSL.
- WSL Debian 13: 19/19 required host commands found; GCC 14.2.0, Python 3.13.5, QEMU 10.0.13; BitBake/bitbake-layers and BUILDDIR absent. Exit 1 correctly means incomplete preflight.
- Full suite PASS: 70 tests on Windows/Python 3.11 and WSL/Python 3.13; compileall and shell syntax on both; `git diff --check` PASS.
