# Test Results

## 2026-10-18 — WSL preflight evidence baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `88fcfc33f8de3dd5ef0808d4161b34888d3f8a63`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Read-only WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; all 19 required host commands present; BitBake/bitbake-layers and BUILDDIR absent; no package changes.
- Static status regression guards firing HEAD, test count and BitBake/QEMU limitations in IT/EN.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse/build, image build or real QEMU boot.
