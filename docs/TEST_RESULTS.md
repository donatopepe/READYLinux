# Risultati test

## 2026-10-18 — Offline Yocto contracts and regression suite

- Runtime recipe test now asserts `inherit allarch`, only repository `file://` application sources, no model/network payload, and its declared Python package dependencies.
- Storico WSL systemd security: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static contracts cover layer metadata and unverified compatibility claims; local recipe sources, package closure and launcher-to-service ExecStart path; getty-mask symlink ownership/image inclusion; READY home, persistent StateDirectory and UMask; plus preflight evidence.
- Relevant regressions pass; full suite: 125 tests PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- No BitBake metadata parse, image build or QEMU boot: host lacks BitBake/OE checkout and `BUILDDIR`; no install/download performed.

## 2026-10-18 — Firing-start snapshot and host probe

- Snapshot iniziale confermato via `git rev-parse HEAD`: `94ec6466d0fa7d01b6b48ffd0405882514251264`; `git status --short --branch` = `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) non tracciati.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
