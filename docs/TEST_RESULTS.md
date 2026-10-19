# Risultati test

## 2026-10-18 — Host preflight firing baseline

- Snapshot iniziale: `git status --short --branch` era `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `8ab20c823363df531c2026b6553496c02fad5962`.
- WSL unit-hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico status controlla snapshot/HEAD, conteggio test e limiti BitBake/QEMU.
- Windows/Python 3.11: 108 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 108 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host probe stub positive/negative copre comandi richiesti e BUILDDIR (unset, valido o file); nessuna installazione/fetch/parse-build BitBake reale.
