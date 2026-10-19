# Risultati test

## 2026-10-18 — Baseline host-preflight WSL

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `eee12774e2408514a6839eaa286de25890fdf4f0`.
- Probe read-only `bash scripts/check-yocto-host.sh` su WSL Debian 13/trixie: exit 1 INCOMPLETE; 19/19 comandi richiesti OK; BitBake/bitbake-layers assenti; QEMU e sha256sum presenti; BUILDDIR unset; nessun package change.
- Test statico status protegge firing HEAD, test count e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun fetch/install, BitBake parse, build immagine, QEMU boot o inference GGUF.
