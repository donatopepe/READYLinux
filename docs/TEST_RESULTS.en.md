# Test Results

## 2026-10-18 — Status/report consistency and current evidence

- IT/EN status explicitly cite the HEAD snapshot at this firing start: `8a287643b5498a307ee8b41e70c85277fcb1b1b0`; they do not claim to identify the HEAD of the later status-update commits.
- Static test checks snapshot commit, BitBake/QEMU limits, MEDIUM exposure/UMask in both files.
- `python -m unittest discover -s tests -v` is the standard full-suite command; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` and `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh` are standard static checks.
- Report records limitations: no real BitBake/Yocto parse/build or QEMU boot performed.
- Windows/Python 3.11: 78 tests PASS (1 expected skip: systemd-analyze unavailable); WSL Debian 13/Python 3.13: 78 tests PASS.
- Compileall, shell syntax on both, and `git diff --check` — PASS.
- No real BitBake/Yocto parse, image build, or QEMU boot performed.
