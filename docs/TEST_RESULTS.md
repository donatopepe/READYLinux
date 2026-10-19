# Risultati test

## 2026-10-18 — Static layer and preflight evidence checks

- Historical WSL unit-security observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Layer metadata regression checks collection/pattern/priority and unique candidate compatibility series. Bilingual README explicitly states these lack release-pinned parse evidence.
- Static preflight-evidence regression checks the firing reports' probe result; recipe/package tests cover getty-mask symlink ownership and inclusion in `FILES`, plus image-installation of the console package that owns it.
- Targeted tests PASS; full suite 123 PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-18 — Firing-start snapshot and host probe

- Snapshot iniziale confermato via `git rev-parse HEAD`: `94ec6466d0fa7d01b6b48ffd0405882514251264`; `git status --short --branch` = `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) non tracciati.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
