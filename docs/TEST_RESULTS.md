# Risultati test

## 2026-10-18 — Regression statici Yocto offline

- Storico WSL systemd security: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Le regression verificano risoluzione `file://` runtime sotto la root repo, search path `FILESEXTRAPATHS` console e uguaglianza senza duplicati di `IMAGE_INSTALL` ai package runtime/consolle.
- Test mirati Windows/WSL PASS; full suite 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot iniziale preflight host

- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `0338faf776a825d08554cd40604098a3125a168a`.
- Probe WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
