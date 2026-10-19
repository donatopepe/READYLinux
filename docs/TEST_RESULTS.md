# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `89d9eaefe92fb24c738e651efcb49889108d53d6`.
- Historical WSL systemd hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- WSL read-only host preflight: exit 1 `INCOMPLETE`, 19/19 comandi richiesti OK; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Static status test protegge firing HEAD e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto, image build o QEMU boot reale.
