# Risultati test

## 2026-10-18 — Baseline WSL host-preflight

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `68ab0f04bbe35b0acef74f04ec7f37200a340003`.
- Storico WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Probe host WSL read-only: exit 1 `INCOMPLETE`; 19/19 comandi required presenti, BitBake/bitbake-layers/BUILDDIR assenti; nessuna modifica ai pacchetti.
- Test static status verifica firing HEAD, test count e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun install/fetch, BitBake parse/build, image build o QEMU boot reale.
