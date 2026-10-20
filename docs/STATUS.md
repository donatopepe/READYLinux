# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 192 test Windows/Python 3.11 (14 skip platform-specific) e WSL Debian 13/Python 3.13; suite, compileall e shell syntax pass. Preflight eseguito dentro WSL Debian 13: 19/19 comandi host richiesti `OK`, `qemu-system-x86_64` trovato, `bitbake`/`bitbake-layers` assenti, `BUILDDIR` unset; exit 1 `INCOMPLETE`. Il probe lanciato dalla shell Windows ora termina con exit 2 `NOT-A-LINUX-HOST` (`WRONG-ENVIRONMENT`) e non viene usato come evidenza (0 = pronto, 1 = `INCOMPLETE`, 2 = ambiente sbagliato). Opzione `--json`: report macchina-leggibile con `verdict` `ready`/`incomplete`/`not-a-linux-host`, mappa comandi e `builddir`; argomenti ignoti exit 64. `scripts/record-yocto-preflight.py OUT.json` registra il report con commit e UTC, rifiuta di scrivere se il preflight non è `ready` (exit 3) non sovrascrive senza `--force` (exit 4) e rifiuta un report che dichiara `ready` con `missing_required` non vuoto o `builddir` non impostata (exit 5). Il record include `preflight_command` e `preflight_exit_code` (0 obbligatorio). Lo schema `docs/YOCTO_PREFLIGHT_RECORD.schema.json` (draft 2020-12) valida il record; `docs/YOCTO_PREFLIGHT_RECORD.example.json` è solo placeholder.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, guest SSH, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; preflight `INCOMPLETE`; nessun checkout/fetch/install.
- **Git**: firing-start HEAD `09f477b87e983bc95ac321e2515f415597b57c52`; contract preflight/schema in `b735cab` e `09f477b`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; aggiornare l'evidence solo dopo parse realmente eseguito.
