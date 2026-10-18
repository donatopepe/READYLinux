# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 85 test Windows (1 skip systemd-analyze) e WSL; compileall/shell/diff pass. Recipe install paths, FILES ownership e audit metadata statico coperti.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: `main` a `4c2dfa0` all'inizio; recipe metadata audit verificato, publish in corso. ZIP ignorati; `.pi-loop.json` locale.
- **Prossimo**: scegliere release/BSP e predisporre BitBake prima di parse/build. Non dichiarare riproducibilità/boot senza evidenze acceptance checklist.
