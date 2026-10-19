# Risultati test

## 2026-10-18 — Baseline firing QEMU helper

- Full-suite command: `python -m unittest discover -s tests -v`.
- HEAD iniziale verificato: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; `git log -1` = `1a4a348cf180e5c43d3d07eae6071ea23b6e364f`.
- WSL systemd security report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Nuovo test simula QEMU exit 23: lo script restituisce lo stesso codice, elimina overlay temporaneo e lascia invariata l'immagine base.
- Windows/Python 3.11: 100 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 100 test PASS.
- `compileall`, `bash -n` e `git diff --check` PASS su entrambi.
- BitBake/Yocto parse/build non eseguiti; boot QEMU reale non fatto.
