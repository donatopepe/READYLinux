# Risultati test

## 2026-10-18 — Test statici Yocto offline

- Storico WSL unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test closure recipe: i `file://` runtime risolvono nella root repository; `FILESEXTRAPATHS` console comprende il service locale; `IMAGE_INSTALL` coincide esattamente con i package runtime/console senza duplicati.
- Test mirato PASS Windows+WSL; suite completa 117 test PASS (8 skip platform-specific) su entrambi.

## 2026-10-18 — Snapshot firing-start preflight WSL

- `git status --short --branch`: `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) untracked; HEAD `ff2612cc6af9639a437e5f22f6b863b985f3ff13`.
- WSL `bash scripts/check-yocto-host.sh` read-only exit 1 `INCOMPLETE`: 19/19 comandi host richiesti presenti, BitBake/bitbake-layers/BUILDDIR assenti, nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
