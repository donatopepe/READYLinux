# Risultati test

## 2026-10-18 — Baseline host-preflight/helper

- Partial-host preflight test keeps a valid BUILDDIR but removes required `gcc`; probe must still report MISSING and INCOMPLETE.
- Static layer-inventory check ensures exactly the intended recipe set and confirms runtime packages are included in `IMAGE_INSTALL`.
- Static layer check pins three expected `.bb` recipes, forbids unreviewed `.bbappend` files, and confirms both runtime packages in `IMAGE_INSTALL`.
- HEAD iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `e235522d23620db53f91ac86e4b9f205ec24fec2`.
- WSL unit-hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static regression test controlla firing HEAD, test count e limiti BitBake/QEMU nei status IT/EN.
- Windows/Python 3.11: 107 test PASS (5 skip platform-specific); WSL Debian 13/Python 3.13: 107 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Host preflight positivo, negative BUILDDIR e helper statici verificati con stubs; nessuna installazione/fetch o build/parse Yocto.
