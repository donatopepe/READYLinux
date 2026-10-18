# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe/BASIC ridotto, scaffolding Yocto e servizio systemd tty1 non-root; helper preflight BitBake, validazione syntax systemd e verifica SHA-256 artifact.
- **Verificato localmente**: 66 test passano su Windows e WSL; compileall/shell syntax su entrambi; unit systemd verificata in WSL; checksum helper testato su fixture.
- **Non verificato**: BitBake/Yocto parse/build, image boot QEMU, hash di artifact READY reale, mascheramento getty nella image, policy runtime completa, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13, 20 CPU logiche, circa 30 GiB RAM WSL; GCC/QEMU x86_64 installati. BitBake assente; nessun checkout/download Yocto eseguito.
- **Git**: `main` sincronizzato con `origin/main`; image checksum helper in verifica. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: pubblicare dopo test Windows/WSL; BitBake/OE setup resta richiesto per parse/build reale; nessun checkout Yocto selezionato.
