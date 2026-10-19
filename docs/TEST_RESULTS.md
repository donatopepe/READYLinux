# Risultati test

## 2026-10-18 — Baseline WSL preflight host

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `84219b5afa145ecc31b9d51a0132f4f2eb86e926`.
- WSL systemd hardening evidence storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status protegge firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- WSL preflight read-only exit 1 `INCOMPLETE`: 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR mancanti; nessuna modifica pacchetti.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto, QEMU boot o inference reale.
