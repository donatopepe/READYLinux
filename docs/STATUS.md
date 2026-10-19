# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: suite+QEMU test con tool fake documentati in `TEST_RESULTS.md`; SSH bridge opt-in attende immagine/server guest, nessun boot SSH reale.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, servizio SSH guest, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; host-preflight read-only exit 1 `INCOMPLETE`: 19/19 required commands OK, QEMU+sha256sum present, BitBake/bitbake-layers absent, BUILDDIR unset; no package changes. No checkout/fetch/install avviato.
- **Git**: firing-start HEAD `4ecf470a867f391f22c5f257c661df6a229242f3`; updated verification plan in `b62cf95`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: metadata parse/build su host OE release-pinned quando disponibile; distinguere fake arguments da boot e guest SSH reali.
