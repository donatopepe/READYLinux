# Test Results

## 2026-10-18 — Local Yocto source closure

- Suite command: `python -m unittest discover -s tests -v`; compileall and `bash -n` shell syntax commands are recorded in the prior baseline entry.
- Added stdlib check reading local `SRC_URI` in each `.bb` recipe and confirming each `file://` source exists in layer/repository or resolved `FILESEXTRAPATHS`.
- Focused test PASS on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- Static source check does not replace BitBake metadata parsing; no QEMU boot run.
- Prior systemd hardening evidence: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Windows/MSYS Python 3.11 suite: 83 tests PASS (1 expected systemd-analyze skip); WSL Debian 13 Python 3.13 suite: 83 tests PASS.
- Compileall, shell syntax and `git diff --check` on both — PASS.
