# Risultati test

## 2026-10-18 — Baseline host-preflight/helper

- New static layer inventory test requires exactly 3 expected `.bb` recipes and no unreviewed `.bbappend` files.
- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `4ba5fef2746f452a5b5a835c9606121c9815415e`.
- WSL unit-hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test controlla firing HEAD, test count e limiti BitBake/QEMU nei status IT/EN.
- Windows/Python 3.11: 105 test PASS (4 skip platform-specific); WSL Debian 13/Python 3.13: 105 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positivo, negative BUILDDIR e helper statici verificati con stubs; nessuna installazione/fetch o build/parse Yocto.
