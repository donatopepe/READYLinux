# Risultati test

## 2026-10-18 — Host preflight evidence baseline

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4a8d047bddf81fb82862ddeb9afb1ce358e96ebf`.
- Historical WSL hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Read-only WSL host probe exit 1 `INCOMPLETE`: Debian 13/trixie x86_64, 20 CPU, 19/19 comandi richiesti presenti, BitBake/bitbake-layers e BUILDDIR mancanti; nessuna modifica ai pacchetti.
- Status regression test protegge firing HEAD, test count e limiti BitBake/QEMU.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Nessun fetch/install, BitBake parse/build o QEMU boot.
