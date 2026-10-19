# Risultati test

## 2026-10-18 — Baseline preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `2b33c9554e7226fb8a08aa9065743aefc92ed3e3`.
- Historical WSL systemd hardening record: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe host WSL read-only: exit 1 `INCOMPLETE`; 19/19 richiesti presenti, BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Status regression protegge HEAD, count test e limiti BitBake/QEMU in IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, parse/build Yocto o boot QEMU reale.
