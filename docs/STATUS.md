# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 99 test Windows (1 skip `systemd-analyze`) e WSL; compileall/shell/diff pass. README clean-build checklist e recipe ownership auditate staticamente.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `7fbe08e17072d45c070c847b14825097228f3dfe`; clean-build checklist guard in verifica. `.pi-loop.json` non tracciato, ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; mantenere audit statici distinti da parse/runtime.
