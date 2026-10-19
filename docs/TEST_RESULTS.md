# Risultati test

## 2026-10-18 — Baseline host preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `3d4b45f09ce21b0bfe887ad06bc9760ade164fa0`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Host probe WSL read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti OK, BitBake/bitbake-layers e BUILDDIR assenti, QEMU+sha256sum presenti; nessuna modifica pacchetti.
- Static status guard verifica firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build BitBake o boot QEMU reale.
