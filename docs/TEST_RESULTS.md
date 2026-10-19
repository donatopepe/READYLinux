# Risultati test

## 2026-10-18 — Regression recipe Yocto offline

- Historical WSL systemd-hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statici verificano risoluzione fonti runtime `file://`, search roots `FILESEXTRAPATHS` console e corrispondenza `IMAGE_INSTALL` ai package runtime/console senza duplicati. Non avviano BitBake/download.
- Test mirato Windows/WSL PASS; suite completa 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot host-preflight firing start

- `git status --short --branch` iniziale: `main...origin/main`, `.pi-loop.json`/`raw` (0 byte) untracked; HEAD `0277c37cba956daf6c830fb0d4d8b80cdc81c306`.
- WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi host richiesti presenti, BitBake/bitbake-layers/BUILDDIR assenti, nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
