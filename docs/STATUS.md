# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 97 test Windows (1 skip `systemd-analyze`) e WSL; compileall/shell/diff pass. DISTRO/MACHINE opt-in e test statici Yocto verificati.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: firing snapshot `0d269c5ea2e8802305dce819c4899e631e049579`; baseline snapshot test pubblicato in `c32761c`. `.pi-loop.json` locale; ZIP ignorati.
- **Prossimo**: parse/build su host OE release-pinned quando selezionato; mantenere distinction tra static audit e metadata parse/runtime.
