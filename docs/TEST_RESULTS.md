# Risultati test

## 2026-10-18 — Baseline path-space validator Yocto

- Snapshot firing: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `58eae291cecf218c3c2ca9568607e8ef89facd85`.
- Historical WSL systemd-security observation: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status regression test verifica firing HEAD, conteggio e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 110 test PASS (7 skip platform-specific); WSL Debian 13/Python 3.13: 110 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Test validator con BUILDDIR spaziato usa BitBake fake: PASS WSL; Windows skip per path temp non condiviso con WSL. Nessun parse/build Yocto reale.
