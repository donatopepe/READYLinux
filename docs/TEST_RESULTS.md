# Risultati test

## 2026-10-18 — Chiusura statica recipe Yocto offline

- Historical WSL systemd-hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test regressione: fonti runtime `file://` risolte nella root repo, search path `FILESEXTRAPATHS` console trova il service e `IMAGE_INSTALL` coincide coi package runtime/console senza duplicati. Verifica offline, senza BitBake/download.
- Test mirati PASS Windows/WSL; suite completa 117 PASS (8 skip platform-specific) su entrambe.

## 2026-10-18 — Preflight host, firing-start

- `git status --short --branch`: `main...origin/main`; `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `65090d4bea45b8d3b86dbffff802891c7d9bb6fd`.
- WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi host presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
