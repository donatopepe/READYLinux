# Test Results

## 2026-10-18 — Verified baseline at firing start

- Current initial snapshot: `git status --short --branch` was `main...origin/main` plus `.pi-loop.json`; HEAD `bb235fdf6c5bd8fe8f6675535f77f8c70976e9d1`.
- License checksum audit checks both MIT recipes use identical `LIC_FILES_CHKSUM` and expected digest; no fabricated MIT content fixture is used.
- Runtime dependency closure checks stdlib imports -> `RDEPENDS` and runtime/console inclusion in `IMAGE_INSTALL`.
- Static SRC_URI extractor now covers URI parameters (`;apply=yes`, `;unpack=0`) and checks the correct local basename; no fetch performed.
- Full-suite command: `python -m unittest discover -s tests -v`.
- Prior WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- IT/EN status refreshed to firing-start HEAD; static test guards hash, test baseline and host limitations.
- Windows/Python 3.11: 98 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 98 tests PASS.
- Verified commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts, and `git diff --check` passed on both.
- No real BitBake/Yocto parse/build or QEMU boot.
