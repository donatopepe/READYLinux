# Risultati test

## 2026-10-18 — Test statici closure recipe offline

- Historical WSL systemd hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Regression: `file://` runtime risolti nella root repository; `FILESEXTRAPATHS` console trova il service file; `IMAGE_INSTALL` corrisponde esattamente ai package runtime/console, senza duplicati. Nessun BitBake/download.
- Test mirato PASS Windows e WSL; suite completa 117 PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot preflight iniziale

- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `c99a6ba15f0d248d71143a6cd73ed8ee51b3efd2`.
- WSL `bash scripts/check-yocto-host.sh` read-only: exit 1 `INCOMPLETE`; 19/19 comandi host presenti, BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, build immagine o boot QEMU reale.
