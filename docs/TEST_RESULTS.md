# Risultati test

## 2026-10-18 — WSL preflight evidence baseline

- Firing-start snapshot: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `88fcfc33f8de3dd5ef0808d4161b34888d3f8a63`.
- Historical WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Probe WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Status regression statica controlla HEAD iniziale, count test e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, BitBake parse/build, image build o boot QEMU reale.
