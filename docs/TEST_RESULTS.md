# Risultati test

## 2026-10-18 — Audit statico ricette Yocto

- Comandi suite/statica: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`.
- Test copre LICENSE=MIT, LIC_FILES_CHKSUM known, runtime RDEPENDS, account `ready`, autostart systemd, assenza AUTOREV e URI remote.
- Windows/Python 3.11 suite: 84 test PASS (1 skip previsto: systemd-analyze assente); WSL Debian 13/Python 3.13 suite: 84 test PASS.
- Nessun BitBake disponibile in apt Debian 13 e nessun checkout Yocto; è audit sorgente, non metadata parse. QEMU boot non eseguito.
- Osservazione systemd host precedente: `systemd-analyze security --offline` MEDIUM/6.7, residuo `UMask 0027`.
- Compileall/shell syntax su entrambi e `git diff --check` — PASS.
