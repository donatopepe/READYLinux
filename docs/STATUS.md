# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, flusso vibe, BASIC ridotto; scaffolding Yocto e servizio systemd READY su tty1.
- **Verificato localmente**: 42 test, compileall, `bash -n`; test statici recipe includono dipendenze Python. Nessun BitBake disponibile.
- **Non verificato**: parse/build/boot Yocto, QEMU, tty1/getty reale, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Ambiente**: Windows/MSYS AMD64, Python 3.11; no download/installazioni.
- **Git**: `main` sincronizzato all'avvio, modifiche packaging in verifica; pubblicare solo whitelist dopo suite verde. ZIP/loop state esclusi.
- **Prossimo**: rendere testabile la risoluzione dei file sorgente `FILESEXTRAPATHS` e documentare variabilità dipendenze OE/Python; poi BitBake su host Linux.
- **Rischi**: unità console tty1 può interferire con getty; non testata in boot reale.
