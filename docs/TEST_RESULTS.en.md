# Test Results

## 2026-10-18 — Isolated QEMU boot helper

- `scripts/boot-image-qemu.sh` requires valid artifact/hash, matching kernel, explicit cmdline; allowlisted machines (`pc`, `q35`, `microvm`); no network/host share/monitor.
- Verifies SHA before boot and uses temporary qcow2 overlay over raw base, preserving original image.
- Negative input/tool/machine/hash and isolation-policy tests; no real QEMU boot (no READY image/kernel available).
- Windows/Python 3.11 suite — PASS, 74 tests; WSL Debian 13/Python 3.13 suite — PASS, 74 tests.
- Compileall and shell syntax on both — PASS; `git diff --check` — PASS.
