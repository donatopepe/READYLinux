# Test Results

## 2026-10-18 — Current baseline, cross-platform validation

- Windows/MSYS, Python 3.11: `python -m unittest discover -s tests -v` — PASS, 66 tests.
- WSL2 Debian 13, Python 3.13: `python3 -m unittest discover -s tests -v` — PASS, 66 tests.
- On both: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` and `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh` — PASS.
- `systemd-analyze verify` on a temporary unit copy with substituted ExecStart — PASS; not image integration/runtime validation.
- `systemd-analyze security --offline`: exposure score 6.7, MEDIUM; residual UMask 0027 documented.
- `git diff --check` — PASS.
- BitBake unavailable; no Yocto parse/build/QEMU boot or real image hash.
