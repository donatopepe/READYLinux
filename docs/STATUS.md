# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, Yocto scaffold, unit systemd tty1 hardenizzata; helper prerequisiti host read-only, preflight BitBake, systemd e checksum image.
- **Verificato localmente**: 70 test su Windows/WSL, compileall/shell syntax/diff check pass. Probe WSL trova 19/19 comandi build, QEMU e versioni package; BitBake/BUILDDIR assenti.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine QEMU, getty mask nell'immagine, comportamento runtime dell'unit, artifact READY reale, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 CPU logiche, 30 GiB RAM WSL, GCC e QEMU x86_64 installati. BitBake non disponibile. Nessun checkout/fetch Yocto effettuato.
- **Git**: `main` sincronizzato con `origin/main`; host probe read-only pubblicato in `561a590`. ZIP e `.pi-loop*` restano non tracciati/esclusi.
- **Prossimo**: scegliere release/BSP e ottenere BitBake su host Linux prima di metadata parse e build; non dichiarare riproducibilità/boot finché checklist README non ha evidenze.
