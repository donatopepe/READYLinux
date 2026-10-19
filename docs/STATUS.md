# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 97 test Windows (1 skip `systemd-analyze`) e WSL; compileall/shell/diff pass. RDEPENDS stdlib e pacchetti image staticamente correlati.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`; dependency closure guard pubblicato in `764c9b4`. ZIP ignorati; `.pi-loop.json` locale.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; distinguere audit statici da parse/runtime.
