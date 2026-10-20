# Test Results

## 2026-10-20 — Preflight evidence correction and 174-test baseline

- `bash scripts/check-yocto-host.sh` run from the Windows shell (Git Bash) is not a Debian host: it reports `/etc/os-release` unavailable and missing tools. That output is not Yocto evidence and must not be recorded.
- Correct command, run inside WSL Debian 13: `wsl -d Debian -- /bin/bash -c 'cd /mnt/d/repos/ReadyLinux && /bin/bash scripts/check-yocto-host.sh'`; exit 1 `INCOMPLETE`, 19/19 required host commands `OK`, `qemu-system-x86_64` and `sha256sum` found, `bitbake`/`bitbake-layers` absent, `BUILDDIR` unset.
- Added a test requiring the IT/EN STATUS files to record the WSL Debian result and forbidding Windows-shell output to be stored as host evidence.
- Full suite: 179 tests PASS (10 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13; `compileall`, `bash -n` and `git diff --check` pass.
- No download, install, BitBake parse, image build or QEMU boot performed.
- New `scripts/record-yocto-preflight.py` records the `--json` report with commit/UTC and a "preflight-only, not build evidence" scope; it refuses to write a non-`ready` verdict (exit 3) or to overwrite without `--force` (exit 4). Suite: 184 tests PASS (13 Windows skips).
- Added `docs/YOCTO_PREFLIGHT_RECORD.schema.json` with a placeholder example and tests for record structure and recorder output; a `ready` verdict must agree with builddir and BitBake. Suite: 188 tests PASS (14 Windows skips).
- `scripts/check-yocto-host.sh` now fails closed on the environment: with no readable `/etc/os-release` it exits 2 `NOT-A-LINUX-HOST` (`WRONG-ENVIRONMENT`), because Windows-shell output is not host evidence. Exit 0 = ready, 1 = `INCOMPLETE`, 2 = wrong environment. Suite: 175 tests PASS.

- Stricter recorder: a report claiming `ready` with non-empty `missing_required` or an unset `builddir` is rejected (exit 5) and nothing is written; 2 tests added. Suite: 190 tests PASS (14 Windows skips).

- Script tracking: `install.sh`, `setup-ai-cpu.sh`, `scripts/*.sh` and `scripts/*.py` were committed as `100644` (not executable); restored `100755` via `git update-index --chmod=+x` and added the `test_tracked_scripts_keep_the_executable_bit` guard. Suite: 191 tests PASS (14 Windows skips).

- Layer README parity: new test compares IT/EN command blocks, `scripts/*.sh|py` references, and that every referenced script exists. Suite: 192 tests PASS.

- Pre-parse gate: `scripts/validate-yocto-env.sh` now rejects a `DISTRO` other than `readylinux` (exit 3) and prints a NOTE when `local.conf` sets no DISTRO; 3 dedicated tests. Suite: 195 tests PASS (17 Windows skips).

## 2026-10-18 — Offline Yocto contracts and regression suite

- Runtime recipe regression asserts `inherit allarch`, repository-local `file://` application sources, no model/network payload and declared Python dependencies. Distro test checks systemd is appended without removing inherited features and is selected as init manager.
- Historical WSL systemd-security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static contracts cover layer metadata and explicitly unverified compatibility candidates; local recipe sources, package closure and launcher-to-service `ExecStart`; getty-mask symlink ownership/image inclusion; READY home, persistent StateDirectory and UMask; plus preflight evidence.
- Relevant regressions pass; full suite: 126 tests PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- No BitBake metadata parse, image build or QEMU boot: BitBake/OE checkout and `BUILDDIR` are absent; no install/download performed.

## 2026-10-18 — Firing-start snapshot and host probe

- Initial snapshot verified by `git rev-parse HEAD`: `92abaae72d9023bb82718ff48e0918ebc17f4b23`; `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes).
- WSL read-only probe `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
