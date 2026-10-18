# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, scaffolding Yocto; servizio tty1 con utente non-root `ready`, state persistente, hardening systemd e unità `getty@tty1` mascherata per evitare concorrenza.
- **Verificato localmente**: 43 test, compileall, `bash -n`, `git diff --check`; test statici verificano mask getty e hardening. BitBake non disponibile.
- **Non verificato**: parse/build/boot Yocto/QEMU, correttezza mapping package, useradd, mascheramento getty, tty1 reale, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; nessun download/installazione.
- **Git**: `main` era sincronizzato a `c9b5b74` all'avvio; mitigazione getty verificata localmente, pubblicazione dopo commit. ZIP e `.pi-loop*` esclusi.
- **Prossimo**: suite completa + commit/push se verde; BitBake/boot su host Linux.
- **Rischio**: getty mask e compatibilità `StateDirectory`/useradd richiedono verifica via BitBake e boot.
