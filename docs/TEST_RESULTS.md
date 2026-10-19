# Risultati test

## 2026-10-18 — WSL Yocto preflight evidence baseline

- Firing snapshot: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `433928a503e426512b5415ec6bb77a0d73314230`.
- Historical WSL hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host preflight WSL è read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti OK, QEMU+sha256sum presenti, BitBake/bitbake-layers e BUILDDIR assenti. No install/fetch.
- Status regression verifica firing HEAD, count test e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun BitBake parse/build, image build, boot QEMU o guest SSH eseguito.
