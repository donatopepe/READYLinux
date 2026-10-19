# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 98 test Windows/Python 3.11 (1 skip `systemd-analyze`) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Test statici license/deps/SRC_URI.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `81298d7dc97c40ab96ac39725d9a0b720b086320`; license/status guard pubblicato in `8d21a02`. `.pi-loop.json` locale, ZIP ignorati.
- **Prossimo**: parse/build su host OE release-pinned quando selezionato; distinguere audit statici da parse/runtime.
