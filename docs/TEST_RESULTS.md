# Risultati test

## 2026-10-18 — Test statico offline ricette Yocto

- Storico WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Il test statico risolve le fonti `file://` della recipe runtime nella root del repository e verifica i percorsi `FILESEXTRAPATHS` della recipe console. Richiede inoltre che `IMAGE_INSTALL` coincida esattamente con i package runtime e console dichiarati, rilevando fonti mancanti e drift dei nomi senza BitBake o download.
- Test mirato PASS su Windows e WSL; suite completa: 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot iniziale preflight host

- `git status --short --branch` iniziale: `main...origin/main`; `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `9c1211592da48bd8f43e87a7d4cff1565a87abe6`.
- WSL `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, build immagine o boot QEMU reale.
