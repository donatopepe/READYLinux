# Risultati test

## 2026-10-18 — Baseline firing QEMU helper

- Full-suite command: `python -m unittest discover -s tests -v`.
- HEAD iniziale verificato: `git status --short --branch` = `main...origin/main` più `.pi-loop.json` non tracciato; `git log -1` = `752a2578cacd309202a36957907634ea6cfb01cd`.
- Nuovo integration test `verify-image-artifact.sh` → fake QEMU eseguito su Windows/Python 3.11 e WSL Debian 13/Python 3.13: PASS.
- Artifact-to-boot integration test verifica checksum prima del fake boot con path image containing spaces; overlay creato/pulito e base image invariata.
- WSL systemd security report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Fake QEMU COW tests materializzano overlay e verificano che esista durante il boot; success case copre path image/kernel con spazi. Exit success/nonzero, cleanup e base image invariance controllati.
- Windows/Python 3.11: 100 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 100 test PASS.
- `compileall`, `bash -n` e `git diff --check` PASS su entrambi.
- BitBake/Yocto parse/build non eseguiti; boot QEMU reale non fatto.
