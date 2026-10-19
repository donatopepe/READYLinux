# Risultati test

## 2026-10-18 — Test statici recipe Yocto offline

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Aggiunto test closure: le fonti `file://` runtime si risolvono nella root repository; i search roots `FILESEXTRAPATHS` console comprendono il service locale; `IMAGE_INSTALL` è esattamente l'insieme package delle ricette runtime/console, senza duplicati. Rileva fonti mancanti e drift nome pacchetto senza BitBake/download.
- Test mirati Windows/WSL PASS; suite completa 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot iniziale preflight WSL

- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `10e7166ab5bcae8fec8a7366edbdd67cc51d8be8`.
- WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi host richiesti presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, build immagine o boot QEMU reale.
