# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 88 test Windows (1 skip systemd-analyze) e WSL; compileall/shell/diff pass. Audit statici coprono source closure, recipe install ownership e IMAGE_INSTALL.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: `main` era a `419fc48`; ownership/image-inclusion tests verificati, publish in corso. ZIP ignorati; `.pi-loop.json` locale.
- **Prossimo**: parse/build su host OE release-pinned quando selezionato; non dichiarare boot/reproducibilità senza acceptance evidence.
