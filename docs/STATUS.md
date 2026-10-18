# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, scaffolding Yocto; servizio tty1 dedicato a utente non privilegiato `ready`, state persistente e hardening systemd di base.
- **Verificato localmente**: suite completa da rieseguire dopo il cambio servizio; BitBake non disponibile.
- **Non verificato**: parse/build/boot Yocto/QEMU, correttezza mapping package sul release target, servizio systemd con useradd, tty1/getty reale, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; nessun download/installazione.
- **Git**: `main` sincronizzato con `origin/main`; servizio non-root pubblicato in `1e1e8f0`. ZIP e `.pi-loop*` esclusi.
- **Prossimo**: test statici hardening/unità + suite completa, poi commit/push; BitBake su host Linux.
- **Rischio**: tty1/getty e compatibilità systemd `StateDirectory` non verificati in boot.
