# Risultati test

## 2026-10-18 — Baseline firing QEMU helper

- Full-suite command: `python -m unittest discover -s tests -v`.
- HEAD iniziale verificato: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; `git log -1` = `286b76eb1654c7fa3a32a0515894aa08ef64ee28`.
- Nuovo test COW path-with-spaces eseguito su Windows/Python 3.11 e WSL Debian 13/Python 3.13: PASS.
- WSL systemd security report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Fake QEMU COW tests materializzano overlay e verificano che esista durante il boot; success case copre path image/kernel con spazi. Exit success/nonzero, cleanup e base image invariance controllati.
- Windows/Python 3.11: 100 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 100 test PASS.
- `compileall`, `bash -n` e `git diff --check` PASS su entrambi.
- BitBake/Yocto parse/build non eseguiti; boot QEMU reale non fatto.
