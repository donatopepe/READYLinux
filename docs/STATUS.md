# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 114 test Windows/Python 3.11 (8 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Preflight WSL read-only ha trovato tutti i comandi host richiesti, ma BitBake/bitbake-layers e BUILDDIR non disponibili.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, SSH guest, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; 19/19 host commands OK, QEMU disponibile; BitBake/bitbake-layers assenti, BUILDDIR unset. Nessun fetch/install.
- **Git**: firing-start HEAD `75b12e66324b51a9631754b63b03a17ebe3f0300`; WSL preflight baseline guard in `0df6b70`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; registrare output completo secondo `docs/VERIFICATION_PLAN.md`.
