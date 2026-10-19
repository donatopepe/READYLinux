# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 117 test Windows/Python 3.11 (8 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Test offline controllano sorgenti locali recipe e chiusura package immagine; BitBake/BUILDDIR assenti.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, guest SSH, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; preflight `INCOMPLETE`; nessun checkout/fetch/install.
- **Git**: firing-start HEAD `c4f4129d76f00c42214edcef632a3e417bfea1f1`; closure/baseline regression in `4f33418`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; registrare output reale secondo `docs/VERIFICATION_PLAN.md`.
