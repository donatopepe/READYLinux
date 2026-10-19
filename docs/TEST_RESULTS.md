# Risultati test

## 2026-10-18 — WSL Yocto preflight baseline

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `ffe6d5b6563c42baaecac7de738767cc2b6089f5`.
- Historical WSL systemd security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host probe WSL read-only: exit 1 `INCOMPLETE`, 19/19 comandi richiesti OK, QEMU+sha256sum presenti, BitBake/bitbake-layers assenti, BUILDDIR unset; nessuna modifica pacchetti.
- Regression status controlla firing HEAD, count suite e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun BitBake parse/build, image build o boot QEMU reale.
