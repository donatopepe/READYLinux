# Test Results

## 2026-10-18 — Verified baseline at firing start

- Full-suite command: `python -m unittest discover -s tests -v`.
- Start snapshot: `git status --short --branch` showed `main...origin/main`; HEAD `95647fd277c41e20357b01c278e9dd9de7440a1`; `.pi-loop.json` untracked.
- Prior systemd finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- IT/EN status aligned to start snapshot; static test protects snapshot, test count and host limitations.
- Windows/Python 3.11: 98 tests PASS (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13: 98 tests PASS.
- Checks: `python -m compileall`; `bash -n` scripts; `git diff --check` pass on both.
- Static coverage includes license checksum, import-to-RDEPENDS closure, IMAGE_INSTALL closure and SRC_URI options.
- License test command: `python -m unittest tests.test_yocto_scaffold.YoctoScaffoldTests.test_license_checksum_is_consistent_across_local_recipes -v`.
- No real BitBake/Yocto parse/build or QEMU boot.
