# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 111 test Windows/Python 3.11 (7 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. QEMU cmdline input-gate verificato con tool stub.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `3fff85ca0c45b62954ff5df2fe0c0255f9daf169`; `.pi-loop.json` e `raw` (0 byte) non tracciati, ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando disponibile; distinguere tool stubs da parse/build/boot reale.
