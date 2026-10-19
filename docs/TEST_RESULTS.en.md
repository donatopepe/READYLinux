# Test Results

## 2026-10-18 — WSL preflight baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `2fa33faaa4311927fdbd788ede95f36d6e74a656`.
- Historical WSL systemd security assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe: exit 1 INCOMPLETE; 19/19 required commands OK; QEMU/sha256sum present; bitbake/bitbake-layers/BUILDDIR absent.
- Static status regression protects firing HEAD, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No install/fetch, BitBake parse, image build, QEMU boot or real inference.
