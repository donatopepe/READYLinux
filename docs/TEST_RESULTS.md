# Risultati test

## 2026-10-18 — Baseline firing e verifica documenti

- Nuovo test QEMU COW failure path: exit status propagato e overlay temporaneo rimosso dopo QEMU simulato nonzero.
- Snapshot iniziale verificato: `git status --short --branch` era `main...origin/main` più `.pi-loop.json` non tracciato; HEAD `23a77ce153a5bfcd347a394c26273d7a3dd4d8b3`.
- Suite completa Windows/Python 3.11 e WSL Debian 13/Python 3.13: 100 test PASS (1 skip systemd-analyze); compileall/shell syntax/diff-check PASS.
- Misura storica WSL `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Test statico controlla snapshot, test count e limiti BitBake/QEMU nei status IT/EN.
- Suite Windows/Python 3.11: 100 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 100 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Build Yocto/parse BitBake e boot QEMU reali non eseguiti.
