# Test Results

## 2026-10-18 — Recipe-source guard baseline

- Initial firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `4a3c4da1e8339070f7a388247340c810bed87332`.
- Historical WSL systemd security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static guard validates firing HEAD, test count and host limitations in status docs.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands run: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Application `file://` recipe source inventory verified statically. No BitBake parse/build, image build or real QEMU boot.
