# Test Results

## 2026-10-18 — Artifact verifier firing baseline

- Initial HEAD: `git status --short --branch` showed `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); `git log -1` = `d622f96c46ca34da204bc42090b97254eeedabee`.
- Historical WSL unit-hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test guards status snapshot/baseline and recorded BitBake/QEMU limitations.
- Windows/Python 3.11: 101 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 101 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier coverage: valid/mismatched digest, malformed input, missing/empty file, symlink/spaced path; does not mutate the artifact.
- No BitBake/Yocto parse/build or real QEMU boot performed.
