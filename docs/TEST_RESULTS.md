# Risultati test

## 2026-10-18 — WSL preflight baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4f1dd4dea369c0ff07265530fbd3ee990995ae87`.
- Historical WSL systemd hardening report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host preflight: exit 1 `INCOMPLETE`; 19/19 comandi required presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica ai pacchetti.
- Static status regression verifica firing HEAD, conteggio test e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o QEMU boot reale.
