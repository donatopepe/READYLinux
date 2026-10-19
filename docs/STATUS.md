# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 114 test Windows/Python 3.11 (8 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Preflight WSL read-only ha rilevato BitBake/bitbake-layers e BUILDDIR mancanti; dettaglio nel verification plan.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, servizio SSH guest, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; 19/19 comandi richiesti presenti, BitBake/bitbake-layers assenti, BUILDDIR unset. Nessun package change/fetch/install.
- **Git**: firing-start HEAD `ffe6d5b6563c42baaecac7de738767cc2b6089f5`; `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; conservare output completo in un record evidence.
