# Test Results

## 2026-10-18 — Static Yocto recipe audit

- Suite/static commands: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`.
- Tests cover MIT license, known `LIC_FILES_CHKSUM`, runtime `RDEPENDS`, `ready` account, systemd autostart, no AUTOREV or remote URIs.
- Windows/Python 3.11 full suite: 84 tests PASS (1 expected systemd-analyze skip); WSL Debian 13/Python 3.13 full suite: 84 tests PASS.
- BitBake has no Debian 13 apt candidate and no Yocto checkout; this is source audit, not metadata parse. No QEMU boot run.
- Prior systemd host observation: `systemd-analyze security --offline` MEDIUM/6.7, residual `UMask 0027`.
- Compileall/shell syntax on both and `git diff --check` — PASS.
