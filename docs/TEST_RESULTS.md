# Risultati test

## 2026-10-18 — Esclusività tty1

- Ricetta console installa symlink `/etc/systemd/system/getty@tty1.service -> /dev/null` perché READY usa tty1.
- Test mirato `python -m unittest tests.test_yocto_scaffold -v` — PASS prima della verifica completa.
- `python -m unittest discover -s tests -v` — PASS, 43 test; compileall, `bash -n` e `git diff --check` — PASS.
- BitBake/QEMU assenti: nessuna verifica reale mascheramento o boot.
