# Risultati test

## 2026-10-18 — Test statici offline Yocto

- Historical WSL systemd hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Nuovo test source/package closure: i `file://` della recipe runtime devono risolversi sotto la root repo; i search roots `FILESEXTRAPATHS` della console devono contenere il service file; `IMAGE_INSTALL` deve coincidere con i pacchetti recipe runtime/console senza duplicati.
- Test mirato PASS su Windows/WSL; suite completa: 117 PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Preflight WSL snapshot

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `5f8d51aa5dfaa62996f14651ca7c7bd71a55bc61`.
- Probe WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Test statico status protegge firing HEAD e limiti host.
- Windows/Python 3.11: 117 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 117 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o boot QEMU reale.
