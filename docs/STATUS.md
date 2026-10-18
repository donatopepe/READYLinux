# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 82 test Windows (1 skip previsto per `systemd-analyze` assente) e 82 WSL; compileall/shell/diff check pass. ZIP ignore e layer override syntax verificati staticamente.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: snapshot firing `f8aa2a57ab050cc054dcfd358e6168e6d678a7d3`; override/ignore test pubblicati in `0794736`. ZIP esclusi; `.pi-loop.json` non tracciato.
- **Prossimo**: scegliere release/BSP e predisporre BitBake prima di parse/build. Non dichiarare riproducibilità/boot senza evidenze acceptance checklist.
