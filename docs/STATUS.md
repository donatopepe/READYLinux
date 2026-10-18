# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release sorgente**: prototype 0.3, ereditato dall'archivio ZIP.
- **Implementato**: console Python numerata, client ai_local, workflow proposte multi-file/diff/approvazione/undo; interprete BASIC esplicito con editing numerato, salvataggio `.bas`, output, variabili, INPUT, condizioni, salti, cicli e subroutine.
- **Verificato**: baseline compileall e 26 test; nuova iterazione compileall, 37 test totali e `bash -n` passati. Interprete BASIC ha test per espressioni, salti, cicli, INPUT, GOSUB/RETURN, persistenza e input non valido.
- **Non implementato/non verificato**: distribuzione Yocto, kernel READY, QEMU, GUI, sandbox reale, inferenza modello GGUF, GPU, ARM64, benchmark.
- **Ambiente**: Windows AMD64, 20 CPU logiche, Python 3.11.7; bitbake/QEMU/containers e compilatori non trovati. RAM non rilevata.
- **Git**: branch `main` sincronizzato con `origin/main`; commit `8ecf8b1` pubblicato. Modifiche successive README/status in lavorazione. ZIP e file loop locali esclusi.
- **Prossimo obiettivo**: M2, costruire scaffolding Yocto minimale e verificabile senza download; documentare comandi host Linux per build/QEMU. Se strumenti non disponibili, avanzare su codice/configurazione e test locali invece di fermare l'intero lavoro.
- **Git policy**: commit/push automatici autorizzati dall'utente per modifiche READYLinux pertinenti; stage solo file whitelisted, mai ZIP, lock, segreti o file estranei. Eseguire test applicabili, poi verificare commit e remote.
- **Limite host OS**: Windows/MSYS corrente non ha BitBake/QEMU; boot immagine non verificabile qui. Continuare comunque attività indipendenti e registrare limite.
