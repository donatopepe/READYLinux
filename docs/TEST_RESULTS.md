# Risultati test

## 2026-10-18 — Offline Yocto source/package closure test

- Added a static closure test requiring local `file://` sources to resolve at documented recipe search roots and image `IMAGE_INSTALL` to equal declared runtime recipe packages. This catches missing source files and package-name drift without BitBake/downloads.
- Targeted test on Windows and WSL passed; full suite result follows below.

## 2026-10-18 — Snapshot preflight WSL

- Snapshot firing-start: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `a2b2036c63f4b8d848bd9ff80885d08cc31aaffa`.
- Historical WSL unit review: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Probe WSL host preflight read-only: exit 1 `INCOMPLETE`; 19/19 comandi richiesti presenti; BitBake/bitbake-layers e BUILDDIR assenti; nessuna modifica pacchetti.
- Test statico status protegge firing HEAD, suite count e limiti BitBake/QEMU.
- Windows/Python 3.11: 117 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 117 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Nessun fetch/install, Yocto parse/build, image build o QEMU boot reale.
