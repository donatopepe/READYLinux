# Risultati test

## 2026-10-18 — Host preflight snapshot baseline

- Snapshot iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `141f86a6893e77903096b2bddc5556ffeca52c7c`.
- Finding storico WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Test statico richiede HEAD, conteggio e limiti BitBake/QEMU negli status IT/EN.
- Windows/Python 3.11: 105 test PASS (4 skip platform-specific); WSL Debian 13/Python 3.13: 105 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Host probe positivo e file-BUILDDIR negativo testati con stub; nessuna installazione, fetch o parse/build BitBake reale.
