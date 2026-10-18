# Risultati test

## 2026-10-18 — Ownership install paths Yocto

- Suite command: `python -m unittest discover -s tests -v`; `python -m compileall`; `bash -n` static shell checks are part of the full run.
- Test statico verifica che ogni path in `do_install` per runtime/service e getty mask sia coperto da `FILES:${PN}` nella recipe corrispondente.
- Controlla anche symlink mask getty e `SYSTEMD_SERVICE` coerente.
- Test mirato Windows/Python 3.11 e WSL Debian 13/Python 3.13 — PASS.
- Non sostituisce package QA/BitBake parse; full suite da rieseguire. QEMU boot non eseguito.
- Finding systemd precedente: `systemd-analyze security --offline`, `MEDIUM/6.7`, UMask 0027.
