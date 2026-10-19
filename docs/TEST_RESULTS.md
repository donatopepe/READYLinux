# Risultati test

## 2026-10-18 — Baseline verificata al firing

- README checklist test confronta DISTRO/MACHINE opt-in, no series mixing, cached-download caveat e ordine parse/build.
- README check asserts opt-in `DISTRO`, BSP `MACHINE` placeholder, series isolation and cached-download caveat appear before metadata parse/build commands.
- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json` non tracciato; HEAD `f22e7b969edbe56de9f4412481daf381d8bd4fe6`.
- WSL systemd hardening observation: `systemd-analyze security --offline`, MEDIUM/6.7, residual UMask 0027.
- Test statico verifica che gli status IT/EN riportino snapshot, baseline e limiti BitBake/QEMU.
- Windows/Python 3.11: 98 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 98 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` sugli script di install/validazione; `git diff --check`.
- Nessun BitBake/Yocto parse/build, package QA o boot QEMU reale.
