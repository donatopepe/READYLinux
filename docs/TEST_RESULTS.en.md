# Test Results

## 2026-10-18 — Package ownership documentation

- Added static check that required systemd unit hardening directives exist and match IT/EN README claims.
- Image recipe audit: MIT license, core-image-minimal base, IMAGE_INSTALL exactly runtime+console, no remote/model refs; distro enables systemd.
- Static image-inclusion audit ensures `IMAGE_INSTALL:append` lists each custom recipe package (runtime + console) exactly once.
- Full-suite command: `python -m unittest discover -s tests -v`; compileall and `bash -n` also run in platform verification.
- IT/EN layer README now state the systemd unit and getty mask are owned by `readylinux-console`, installed by image recipe.
- Static test cross-checks those statements against recipe `RDEPENDS`, `FILES:${PN}`, and installed symlink/unit paths; image-inclusion audit checks runtime and console appear once in `IMAGE_INSTALL`.
- Prior systemd hardening finding: `systemd-analyze security --offline`, `MEDIUM/6.7`, `UMask 0027`.
- Windows/Python 3.11 full suite — PASS, 90 tests (1 systemd-analyze skip); WSL Debian 13/Python 3.13 full suite — PASS, 90 tests.
- Compileall, shell syntax on both, `git diff --check` — PASS.
- No BitBake/package QA available; no real QEMU boot.
