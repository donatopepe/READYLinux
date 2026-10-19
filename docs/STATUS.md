# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: suite+QEMU test con tool fake documentati in `TEST_RESULTS.md`; SSH bridge opt-in attende immagine/server guest, nessun boot SSH reale.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, servizio SSH guest, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `b95b50d4e5d6524886ae78adece54500aca99ffb`; verification-gap plan published in `b95b50d`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando disponibile; distinguere fake arguments da boot e guest SSH reali.
