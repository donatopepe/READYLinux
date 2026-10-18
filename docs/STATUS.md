# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 79 test su Windows/Python 3.11 (1 skip systemd-analyze assente) e WSL/Python 3.13; compileall/shell/diff check pass. systemd verify/security MEDIUM/6.7, UMask 0027; fake QEMU COW cleanup pass.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti, BitBake assente; nessun checkout/fetch Yocto.
- **Git**: snapshot a inizio firing `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`; successivi commit di questo firing aggiornano test/status. ZIP e `.pi-loop*` esclusi.
- **Prossimo**: scegliere release/BSP e predisporre BitBake prima di parse/build. Non dichiarare riproducibilità/boot senza evidenze acceptance checklist.
