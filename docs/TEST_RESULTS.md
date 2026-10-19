# Risultati test

## 2026-10-18 — Regression statica offline Yocto

- Storico WSL unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Verifica closure locale: `file://` della recipe runtime risolti nella repo; `FILESEXTRAPATHS` console trova il service; `IMAGE_INSTALL` equivale ai due package runtime/console senza duplicati.
- Test mirati Windows/WSL PASS; suite completa 117 PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot iniziale preflight host

- `git status --short --branch`: `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `b3b8e74017885f1da899cabe3b60fd49c802ec91`.
- WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
