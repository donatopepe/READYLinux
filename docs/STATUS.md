# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 97 test Windows/Python 3.11 (1 skip `systemd-analyze`) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. SRC_URI parsing statico include URI options `;apply`/`;unpack`.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: snapshot firing `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`; SRC_URI option guard pubblicato in `c088bf1`. ZIP ignorati; `.pi-loop.json` locale.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; distinguere audit statici da parse/runtime.
