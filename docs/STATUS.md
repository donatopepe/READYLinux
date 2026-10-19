# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 104 test Windows (3 skip: `systemd-analyze`, FIFO POSIX, host probe PATH POSIX) e WSL; SHA-mismatch QEMU gate lascia l'immagine base invariata.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `e930fff2e4b3d1efb8c19141bb875625fdfb1f0f`; rejected-image immutability test verificato, publish in corso. `.pi-loop.json` e `raw` (0 byte) non tracciati, ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; distinguere test stub da host build reale.
