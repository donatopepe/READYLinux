# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe/BASIC ridotto, scaffolding Yocto e servizio systemd tty1 non-root; helper preflight BitBake e validazione locale unità systemd.
- **Verificato localmente**: 62 test passano su Windows e WSL; compileall/shell syntax su entrambi; unit file accettato da `systemd-analyze verify` su WSL Debian 13.
- **Non verificato**: BitBake/Yocto parse/build, image boot QEMU, mascheramento getty nella image, policy runtime completa, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13, 20 CPU logiche, circa 30 GiB RAM WSL; GCC/QEMU x86_64 installati. BitBake assente; nessun checkout/download Yocto eseguito.
- **Git**: `main` sincronizzato con `origin/main`; systemd validation helper pubblicato in `77c6704`. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: eseguire suite Windows + WSL e pubblicare; valutare helper BitBake non intrusivo per Debian.
