# Risultati test

## 2026-10-18 — Host preflight firing baseline

- Snapshot iniziale: `git status --short --branch` era `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `afd0d88293cb73d83fa219356b5bb54722d90c34`.
- WSL unit-hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status controlla snapshot/HEAD, conteggio test e limiti BitBake/QEMU.
- Windows/Python 3.11: 108 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 108 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight stub covers valid/missing/file/nonexistent BUILDDIR and missing required tool; no install/fetch/real BitBake parse/build.
