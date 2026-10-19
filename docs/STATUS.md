# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 101 test Windows (1 skip `systemd-analyze`) e WSL; compileall/shell/diff pass. Artifact verify→fake QEMU integrato con immagine/kernel dai path spaziati.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `752a2578cacd309202a36957907634ea6cfb01cd`; artifact-to-fake-boot integration test pubblicato in `60a49ab`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando selezionato; tenere test simulati distinti dalle verifiche hardware/build reali.
