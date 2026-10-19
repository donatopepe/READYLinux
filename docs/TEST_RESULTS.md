# Risultati test

## 2026-10-18 — Host probe Yocto

- Full suite command: `python -m unittest discover -s tests -v`.
- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json`/`raw` non tracciati; HEAD `088d7f42bcc37fba1f1d8edca5a68332c757a888`.
- WSL systemd hardening finding storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico verifica snapshot e conteggio test nel status IT/EN.
- Windows/Python 3.11: 104 test PASS (3 skip: `systemd-analyze`, FIFO POSIX, PATH-stub probe POSIX); WSL Debian 13/Python 3.13: 104 test PASS.
- Suite completa e `compileall`, `bash -n`, `git diff --check` eseguiti su entrambi.
- Host probe successo/fallimento testato con command stub; BitBake e QEMU assenti, nessun install/fetch o build Yocto reale.
