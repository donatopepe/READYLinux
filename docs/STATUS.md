# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 114 test Windows/Python 3.11 (8 skip platform-specific) e WSL Debian 13/Python 3.13; compileall/shell/diff pass. Host-probe WSL ha 19/19 requisiti ma BitBake/BUILDDIR assenti.
- **Non verificato**: BitBake/Yocto parse/build reale, boot immagine READY QEMU, SSH guest, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: WSL Debian 13/trixie x86_64, 20 CPU; preflight INCOMPLETE, nessun checkout/fetch/install.
- **Git**: firing-start HEAD `e35f40e014b706e04f53cf09eaed0b37d12fdf2f`; host-preflight/status snapshot guard in `78fecd9`. `.pi-loop.json` e `raw` (0 byte) non tracciati; ZIP ignorati.
- **Prossimo**: Gate A parse su host OE release-pinned già provisionato; conservare stdout, stderr e commit/versione esatta nel build-evidence record.
