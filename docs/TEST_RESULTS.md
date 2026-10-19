# Risultati test

## 2026-10-18 — Baseline artifact verifier firing

- New QEMU gate test confirms a valid-format but mismatched SHA-256 exits before qemu-img/QEMU invocation.
- HEAD iniziale: `git status --short --branch` mostrava `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; `git log -1` = `b98084d81e9cebe6e720cad48a5e37593c3d631f`.
- WSL hardening report storico: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Test statico controlla status snapshot/baseline e dichiarazione limiti BitBake/QEMU.
- Windows/Python 3.11: 103 test PASS (2 skip: `systemd-analyze` + FIFO test POSIX); WSL Debian 13/Python 3.13: 103 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Artifact verifier: digest valido/mismatch, forma input, file mancante/vuoto, FIFO Unix (skip Windows), symlink/path spaziato; nessuna mutazione artifact.
- BitBake/Yocto parse/build e boot QEMU reale non eseguiti.
