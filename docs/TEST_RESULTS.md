# Risultati test

## 2026-10-18 — Test layer Yocto e preflight statico

- Storico WSL unit hardening: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test layer: controlla collection/pattern/priorità, serie compatibilità uniche, e dichiarazione nei README IT/EN che le serie candidate restano non validate fino a parse release-pinned.
- Suite completa: 122 test PASS, 8 skip platform-specific, su Windows e WSL.

## 2026-10-18 — Snapshot firing-start

- Snapshot SHA1 iniziale `git rev-parse HEAD`: `94ec6466d0fa7d01b6b48ffd0405882514251264`.
- `git status --short --branch`: `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) untracked.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi host presenti; BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica pacchetti.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Nessun parse/build Yocto, image build o boot QEMU reale.
