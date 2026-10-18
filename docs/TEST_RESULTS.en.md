# Test Results

## 2026-10-18 — Git snapshot and updated baseline

- At firing start, `git status --short --branch` showed `main...origin/main`; HEAD `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`.
- IT/EN status documents this initial snapshot; later commits in this firing update tests/status, not the observed start snapshot.
- Commands actually run: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Static tests verify report linkage and recorded BitBake/QEMU/systemd limitations.
- systemd exposure captured from WSL: `systemd-analyze security --offline`, MEDIUM/6.7, residual UMask 0027.
- Windows/Python 3.11 suite: 79 tests PASS (1 expected skip: systemd-analyze unavailable); WSL Debian 13/Python 3.13 suite: 79 tests PASS.
- On both: compileall, shell syntax and `git diff --check` PASS.
- No BitBake/Yocto parse, image build or READY QEMU boot performed.
