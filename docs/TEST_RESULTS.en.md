# Test Results

## 2026-10-18 — Image artifact verification for QEMU

- Image checksum helper added at `scripts/verify-image-artifact.sh`; validates file/hash only and does not launch QEMU.
- Windows/Python 3.11 suite — PASS, 66 tests; WSL Debian 13/Python 3.13 suite — PASS, 66 tests.
- Compileall and `bash -n` on both — PASS; WSL `systemd-analyze verify` — PASS; `git diff --check` — PASS.
- No READY image artifact exists; helper not run against a real image.

## 2026-10-18 — Image artifact verification

- Added `scripts/verify-image-artifact.sh`: requires non-empty regular file and expected SHA-256; returns 0 match, 1 mismatch, 2 invalid input/tool. Does not invoke QEMU or create artifacts.
- Tests digest match/mismatch, malformed digest, missing/empty image.
- Windows/Python 3.11 suite — PASS, 66 tests; WSL Debian 13/Python 3.13 suite — PASS, 66 tests.
- Compileall and shell syntax on both — PASS; `git diff --check` — PASS.
- No READY image exists to verify.
