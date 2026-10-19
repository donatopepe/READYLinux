# Risultati test

## 2026-10-18 — Baseline firing QEMU helper

- Full-suite command: `python -m unittest discover -s tests -v`.
- HEAD iniziale verificato: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; `git log -1` = `05c60562680e6b5b9ef8d371beff878a82c0ad39`.
- WSL systemd security report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Fake QEMU COW tests materializzano overlay; fake QEMU ne verifica esistenza durante il boot. Copertura exit success/nonzero, cleanup e immagine base invariata.
- Windows/Python 3.11: 100 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 100 test PASS.
- `compileall`, `bash -n` e `git diff --check` PASS su entrambi.
- BitBake/Yocto parse/build non eseguiti; boot QEMU reale non fatto.
