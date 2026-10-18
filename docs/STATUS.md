# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, proposte vibe/diff/approvazione/undo, runtime BASIC ridotto; scaffolding Yocto con ricetta runtime e immagine, servizio systemd avvio automatico READY su tty1.
- **Verificato localmente**: 42 test, compileall, `bash -n`, controlli statici layer/ricette/unità; nessun BitBake disponibile.
- **Non verificato**: parse/build BitBake, boot QEMU, tty1/getty interazione reale, kernel, modello GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; BitBake/QEMU assenti. Nessun download o installazione eseguiti.
- **Git**: `main` sincronizzato con `origin/main` prima di questa unità; pubblicare modifiche whitelist dopo test. ZIP e loop state esclusi.
- **Prossimo**: migliorare test statici recipe e gestire dipendenze Python/package; poi validation BitBake su host Linux.
- **Rischi noti**: unità tty1 assume systemd proprietario del terminale; possibili conflitti con getty non esclusi senza boot.
