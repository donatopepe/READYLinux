# Test Results

## 2026-10-18 — WSL host-preflight baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `eee12774e2408514a6839eaa286de25890fdf4f0`.
- Read-only `bash scripts/check-yocto-host.sh` on WSL Debian 13/trixie: exit 1 INCOMPLETE; 19/19 required commands OK; BitBake/bitbake-layers absent; QEMU and sha256sum found; BUILDDIR unset; no package changes.
- Static status test guards firing HEAD, suite count and BitBake/QEMU limitations.
- Windows/Python 3.11: 114 tests PASS (8 platform-specific skips); WSL Debian 13/Python 3.13: 114 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- No fetch/install, BitBake parse, image build, QEMU boot or GGUF inference.
