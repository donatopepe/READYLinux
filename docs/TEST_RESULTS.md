# Risultati test

## 2026-10-18 — Snapshot Git e baseline aggiornata

- A inizio firing: `git status --short --branch` indicava `main...origin/main`; HEAD `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`.
- IT/EN status documentano questo snapshot iniziale; i commit successivi del firing aggiornano test/status, non lo snapshot osservato.
- Comandi realmente eseguiti: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- Test statici verificano il legame ai report e la registrazione dei limiti BitBake/QEMU/systemd.
- Esposizione systemd acquisita su WSL: `systemd-analyze security --offline`, MEDIUM/6.7, residuo UMask 0027.
- Windows/Python 3.11 suite: 79 test PASS (1 skip previsto: systemd-analyze assente); WSL Debian 13/Python 3.13 suite: 79 test PASS.
- In entrambi: compileall, shell syntax e `git diff --check` PASS.
- BitBake/Yocto parse, build immagine e QEMU boot READY non eseguiti.
