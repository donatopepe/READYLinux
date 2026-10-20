# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 156 test Windows/Python 3.11 (8 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Guard useradd verifica package scope e parametri singoli per account/gruppo sistema. BitBake/BUILDDIR assenti.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, guest SSH, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; preflight `INCOMPLETE`; nessun checkout/fetch/install.
- **Git**: firing-start HEAD `92abaae72d9023bb82718ff48e0918ebc17f4b23`; evidence-example verification-state contract in `545c14e`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; aggiornare l'evidence solo dopo parse realmente eseguito.
