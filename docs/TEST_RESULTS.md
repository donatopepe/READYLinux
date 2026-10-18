# Risultati test

## 2026-10-18 — Helper boot QEMU isolato

- `scripts/boot-image-qemu.sh` richiede artifact/hash validi, kernel matching e cmdline espliciti; machine allowlist (`pc`, `q35`, `microvm`); nessuna rete/host share/monitor.
- Verifica SHA prima del boot e usa overlay qcow2 temporaneo sopra base raw, per non modificare l'immagine originale.
- Fake QEMU/qemu-img test conferma overlay temporaneo rimosso dopo uscita QEMU e base image invariata; test negativi coprono input/tool/machine/hash. Nessun QEMU boot reale (image/kernel READY assenti).
- Windows/Python 3.11 suite — PASS, 75 test; WSL Debian 13/Python 3.13 suite — PASS, 75 test.
- Compileall e shell syntax su entrambi — PASS; `git diff --check` — PASS.
