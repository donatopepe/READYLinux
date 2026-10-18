# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, Yocto scaffold, unit tty1 hardenizzata; helper host preflight, BitBake, systemd, checksum image e boot QEMU isolato/COW.
- **Verificato localmente**: 75 test su Windows/WSL; fake QEMU conferma overlay COW temporaneo rimosso e image base invariata; nessun image/kernel READY reale.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine QEMU, getty mask nell'immagine, comportamento runtime dell'unit, artifact READY reale, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 CPU logiche, 30 GiB RAM WSL, GCC e QEMU x86_64 installati. BitBake non disponibile. Nessun checkout/fetch Yocto effettuato.
- **Git**: `main` era a `b23c709`; QEMU COW flow verificato con fake, publish in corso. ZIP e `.pi-loop*` restano non tracciati/esclusi.
- **Prossimo**: scegliere release/BSP e ottenere BitBake su host Linux prima di metadata parse e build; non dichiarare riproducibilità/boot finché checklist README non ha evidenze.
