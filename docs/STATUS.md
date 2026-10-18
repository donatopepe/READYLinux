# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: suite aggiornata 78 test Windows/Python 3.11 (1 skip atteso: systemd-analyze assente) e 78 test WSL/Python 3.13; compileall, bash syntax e diff check pass. Unit systemd e fake QEMU COW verificati.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: main era allineato a `origin/main` a inizio firing sullo snapshot `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`; i commit di aggiornamento documenti di questo firing seguono quello snapshot. ZIP e `.pi-loop*` restano esclusi.
- **Prossimo**: scegliere release/BSP e predisporre BitBake prima di parse/build. Non dichiarare riproducibilità/boot senza evidenze acceptance checklist.
