# Test Results

## 2026-10-18 — Artifact verifier firing baseline

- New QEMU gate test confirms valid-format SHA-256 mismatch exits before invoking qemu-img or QEMU.
- Initial HEAD: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `7b052859821ad357e77aa89b8f580bb78a2dd1e7`.
- Historical WSL unit-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test guards status snapshot/baseline and recorded BitBake/QEMU limitations.
- Windows/Python 3.11: 102 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 102 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier coverage: valid/mismatched digest, malformed input, missing/empty file, symlink/spaced path; does not mutate the artifact.
- No BitBake/Yocto parse/build or real QEMU boot performed.
