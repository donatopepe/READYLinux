# Test Results

## 2026-10-18 — Test/status baseline

- Added static IT/EN test for tty1 ownership, getty mask and absence of a normal login prompt.

- HEAD snapshot at firing start: `6266983bc1ce4aaaf9cd60a9b8158fa79276daf9`; static test requires IT/EN status to cite snapshot, current baseline and BitBake/QEMU limitations.
- Full Windows/Python 3.11 suite — PASS, 94 tests (1 `systemd-analyze` skip); WSL Debian 13/Python 3.13 — PASS, 94 tests.
- `compileall`, shell syntax on both, and `git diff --check` — PASS.

## 2026-10-18 — Package ownership documentation

- Added static test: unit/recipe assign `/dev/tty1` to READY, mask `getty@tty1.service`, and both READMEs explain reserved tty/no login prompt.
- User/group/state test checks unit `User`/`Group` and `StateDirectory=readylinux` against USERADD/GROUPADD, persistent path, and mode 0750.
- Writable-state scope test: `StateDirectory=readylinux`, `ReadWritePaths=/var/lib/readylinux`, XDG state path align; broad writable paths rejected.
- Added static assertion that `StateDirectory`, `ReadWritePaths` and `XDG_DATA_HOME` stay scoped to `/var/lib/readylinux` and avoid broad writable paths (`/home`, `/etc`, `/usr`, `/opt`).
- Added static check that required systemd unit hardening directives exist and match IT/EN README claims.
- Image recipe audit: MIT license, core-image-minimal base, IMAGE_INSTALL exactly runtime+console, no remote/model refs; distro enables systemd.
- Static image-inclusion audit ensures `IMAGE_INSTALL:append` lists each custom recipe package (runtime + console) exactly once.
- Full-suite command: `python -m unittest discover -s tests -v`; compileall and `bash -n` also run in platform verification.
- IT/EN layer README now state the systemd unit and getty mask are owned by `readylinux-console`, installed by image recipe.
- Static test cross-checks those statements against recipe `RDEPENDS`, `FILES:${PN}`, and installed symlink/unit paths; image-inclusion audit checks runtime and console appear once in `IMAGE_INSTALL`.
- Prior systemd hardening finding: `systemd-analyze security --offline`, `MEDIUM/6.7`, `UMask 0027`.
- Windows/Python 3.11 full suite — PASS, 93 tests (1 systemd-analyze skip); WSL Debian 13/Python 3.13 full suite — PASS, 93 tests.
- Compileall, shell syntax on both, `git diff --check` — PASS.
- No BitBake/package QA available; no real QEMU boot.
