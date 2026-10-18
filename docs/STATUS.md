# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 91 test Windows (1 skip systemd-analyze) e WSL; compileall/shell/diff pass. Writable paths staticamente limitati al state persistente; hardening README/unit coerente.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: snapshot firing `0af873121688d50fd187afb01f3bd671d4be2ab7`; writable-state guard pubblicato in `a547aef`. ZIP ignorati; `.pi-loop.json` locale.
- **Prossimo**: parse/build su host OE release-pinned quando selezionato; non dichiarare boot/reproducibilità senza acceptance evidence.
