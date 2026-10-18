# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release sorgente**: prototype 0.3, ereditato dall'archivio ZIP.
- **Implementato**: console Python numerata, client ai_local, workflow proposte multi-file/diff/approvazione/undo; interprete BASIC esplicito in `basic.py` con modalità console, salvataggio `.bas`, test dedicati.
- **Verificato**: baseline compileall e 26 test; nuova iterazione compileall, 37 test totali e `bash -n` passati. Interprete BASIC ha test per espressioni, salti, cicli, INPUT, GOSUB/RETURN, persistenza e input non valido.
- **Non implementato/non verificato**: distribuzione Yocto, kernel READY, QEMU, GUI, sandbox reale, inferenza modello GGUF, GPU, ARM64, benchmark.
- **Ambiente**: Windows AMD64, 20 CPU logiche, Python 3.11.7; bitbake/QEMU/containers e compilatori non trovati. RAM non rilevata.
- **Git**: branch main, nessun commit; remote READYLinux.git. ZIP mantenuti come input locali, non pubblicare senza richiesta.
- **Prossimo obiettivo**: rafforzare test negativi e documentazione BASIC; M1 resta aperta finché i comandi legacy richiesti e l'esperienza end-to-end non sono verificati.
- **Git policy**: richiesta utente per commit/push automatici dopo test verdi; push non ancora eseguito, autenticazione non verificata. ZIP e lock locali esclusi.
- **Blocco OS**: build Yocto/QEMU necessita host/toolchain Linux adeguati; non installare toolchain o scaricare componenti senza autorizzazione.
