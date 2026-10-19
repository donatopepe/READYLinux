# Risultati test

## 2026-10-18 — Test offline di chiusura recipe Yocto

- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Le regression statiche verificano risoluzione runtime `file://` sotto la root repository, search path `FILESEXTRAPATHS` del service console e uguaglianza esatta del set `IMAGE_INSTALL` ai package runtime/console.
- Test mirati Windows/WSL PASS; suite completa 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot firing-start preflight WSL

- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `c4f4129d76f00c42214edcef632a3e417bfea1f1`.
- WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti, BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, build image o boot QEMU reale.
