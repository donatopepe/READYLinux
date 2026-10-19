# Risultati test

## 2026-10-18 — Static tests closure recipe Yocto

- Nuovo test layer metadata: controlla collection, pattern `${LAYERDIR}`, priorità positiva e lista unica di serie Yocto supportate; non seleziona una release specifica senza parse reale.

- Storico WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Regression offline: risoluzione `file://` runtime alla root repo; search path `FILESEXTRAPATHS` console per il service; `IMAGE_INSTALL` coincide coi package runtime/console senza duplicati.
- Test mirati Windows/WSL PASS; suite completa 117 PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot firing-start WSL preflight

- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `e1372e6799214fd26648883acc0416acae9a7c8f`.
- Probe WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica ai pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, build image o boot QEMU reale.
