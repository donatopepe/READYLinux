# Risultati test

## 2026-10-18 — Probe prerequisiti Yocto read-only

- `scripts/check-yocto-host.sh` rileva distro/arch/CPU, comandi host richiesti, versioni pacchetti chiave, BitBake/QEMU e BUILDDIR; non installa né scarica.
- Test mirati `python -m unittest tests.test_yocto_host_check -v` — PASS, 4 test su Windows e WSL.
- WSL Debian 13: 19/19 comandi host richiesti trovati; GCC 14.2.0, Python 3.13.5, QEMU 10.0.13; BitBake/bitbake-layers e BUILDDIR assenti. Exit 1 significa preflight incompleto.
- Suite completa: PASS, 70 test su Windows/Python 3.11 e WSL/Python 3.13; compileall e shell syntax su entrambi, `git diff --check` PASS.
