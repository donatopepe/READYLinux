# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, scaffolding Yocto e servizio tty1.
- **Verificato localmente**: test launcher/recipe mirati passati; suite completa da rieseguire. BitBake non disponibile.
- **Non verificato**: parse/build/boot Yocto/QEMU, correttezza mapping package sul release target, tty1/getty reale, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; nessun download/installazione.
- **Git**: `main` sincronizzato con `origin/main` a `ac7cd37` all'avvio; launcher fix in verifica. ZIP e `.pi-loop*` esclusi.
- **Prossimo**: verificare dipendenze runtime e documentare la variabilità OE per release; BitBake su Linux resta follow-up.
