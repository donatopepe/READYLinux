# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 111 test Windows (7 skip platform-specific) e WSL; QEMU helper rifiuta cmdline kernel vuota prima dei tool. Nessun boot reale.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `a0be463c6e46d433e3db08bba29743d43d10d2c1`; empty-kernel-cmdline QEMU guard pubblicato in `93c17dc`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando disponibile; distinguere fake BitBake da parse/build reale.
