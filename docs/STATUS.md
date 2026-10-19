# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 103 test Windows/Python 3.11 (2 skip: `systemd-analyze`, FIFO POSIX) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Artifact verifier rifiuta FIFO Unix.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `498d96875365fa45ec895bb23b6f46e7168875ee`; snapshot guard pubblicato in `e9cc227`. `.pi-loop.json` e `raw` (0 byte) non tracciati, ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; separare test helper da build/hardware reali.
