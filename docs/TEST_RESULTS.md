# Risultati test

## 2026-10-18 — Baseline verificata al firing

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json` non tracciato; HEAD `d9c8f9ab6d9832741a38c29f34dac2a3e2d80318`.
- WSL systemd hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, residual UMask 0027.
- Test statico verifica che gli status IT/EN riportino snapshot, baseline e limiti BitBake/QEMU.
- Windows/Python 3.11: 98 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 98 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` sugli script di install/validazione; `git diff --check`.
- Nessun BitBake/Yocto parse/build, package QA o boot QEMU reale.
