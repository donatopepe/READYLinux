# Risultati test

## 2026-10-18 — Verification gap audit / SSH forward baseline

- Read-only `bash scripts/check-yocto-host.sh`: exit 1, Debian 13/trixie x86_64, 20 CPUs, 19 required host commands OK, optional QEMU+sha256sum found, BitBake/bitbake-layers absent, BUILDDIR unset; no package changes.
- Verification plan `docs/VERIFICATION_PLAN.md` decomposes all open status items into gates, prerequisites, commands and pass evidence. No gates were falsely upgraded: no BitBake, image, guest SSH or inference run happened.
- Firing-start snapshot: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4ecf470a867f391f22c5f257c661df6a229242f3`.
- Historical WSL hardening check: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression test tutela firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- SSH QEMU forwarding opt-in e loopback-only validato solo sugli arg fake; nessun guest SSH o boot reale. No Yocto parse/build.
