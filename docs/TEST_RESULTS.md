# Risultati test

## 2026-10-18 — Closure sorgenti locali Yocto

- Suite command: `python -m unittest discover -s tests -v`; compileall command documented in previous baseline; shell command `bash -n` documented there too.
- Aggiunto controllo stdlib che legge `SRC_URI` locale di ogni recipe `.bb` e verifica che ogni `file://` abbia sorgente nel layer/repository o nella FILESEXTRAPATHS risolta.
- Test mirato PASS su Windows/Python 3.11 e WSL Debian 13/Python 3.13.
- Questo è controllo statico sorgenti, non sostituisce il parse BitBake; nessun QEMU boot eseguito.
- Evidenza hardening precedente: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Windows/MSYS Python 3.11 suite: 83 test PASS (1 skip previsto: systemd-analyze assente); WSL Debian 13 Python 3.13 suite: 83 test PASS.
- Compileall, shell syntax e `git diff --check` su entrambi — PASS.
