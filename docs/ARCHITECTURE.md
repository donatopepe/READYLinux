# Architettura READY Linux (proposta incrementale)

## Stato attuale

Applicazione Python: `readylinux.py` gestisce console READY, programmi numerati Python e modalità BASIC esplicita; `basic.py` implementa runtime BASIC con valutatore espressioni AST ristretto; `ai_local.py` chiama server llama.cpp locale; `vibe.py` gestisce workspace, proposte multi-file, diff/applicazione/rollback e controlli statici. Test in `tests/`. Nessun livello OS, kernel, GUI, sandbox o build embedded presente.

## Yocto boot path (scaffold)

The `readylinux-console` systemd unit starts `/usr/bin/readylinux` on `/dev/tty1`, restarts on failure, and is enabled in the minimal image. It assumes systemd owns tty1; getty conflict, user/session policy, and actual boot are unverified. No AI model service starts at boot.

## Hardware and model selection

Capacity-based purchasing guidance and the model provenance/verification policy are in [`AI_HARDWARE.it.md`](AI_HARDWARE.it.md) and [English](AI_HARDWARE.en.md). Current tiers are estimates only, not web-researched product recommendations; model selection must remain opt-in and verifiable.

## Target

1. **Classic runtime**: shell READY indipendente dall'IA e runtime BASIC reale, poi console primaria su Linux.
2. **Project agent**: interfaccia astratta per inferenza locale; modifiche solo come patch approvabili; runner isolato reale.
3. **System image**: layer Yocto separato da runtime; Stable prima, Performance solo dopo benchmark; immagini x86-64 e ARM64 distinte.
4. **UI**: processi separati per interfaccia e inference, protocollo locale documentato; Classic resta accessibile senza GUI.

## Confini di sicurezza

Il modello non ottiene accesso filesystem generale né privilegi. I controlli statici non equivalgono a sandbox. Codice generato non attendibile resta non eseguibile automaticamente finché un runner isolato e testato non è disponibile. Niente download di modelli o toolchain durante build base.

## Decisioni aperte

Yocto release/BSP, linguaggio BASIC, GUI toolkit, sandbox runtime, modelli e formati protocollo vanno scelti con spike misurabili, non assunti.
