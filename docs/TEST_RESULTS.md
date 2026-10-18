# Risultati test

## 2026-10-18 — Ownership install paths Yocto

- Suite command: `python -m unittest discover -s tests -v`; compileall and shell syntax also part of the cross-host run.
- Suite command: `python -m unittest discover -s tests -v`; `python -m compileall`; `bash -n` static shell checks are part of the full run.
- Test statico verifica che ogni path in `do_install` per runtime/service e getty mask sia coperto da `FILES:${PN}` nella recipe corrispondente.
- Controlla anche symlink mask getty e `SYSTEMD_SERVICE` coerente.
- Suite Windows/Python 3.11 — PASS, 86 test (1 skip systemd-analyze); suite WSL Debian 13/Python 3.13 — PASS, 86 test.
- Test non sostituisce package QA/BitBake parse. QEMU boot non eseguito.
- Compileall, shell syntax su entrambi, `git diff --check` — PASS.
- Finding systemd precedente: `systemd-analyze security --offline`, `MEDIUM/6.7`, UMask 0027.
