# Stato READY Linux

Aggiornato: 2026-10-18.

Nota: gli archivi ZIP locali sono esclusi da Git (`*.zip`); possono restare non tracciati.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 100 test Windows e WSL (1 skip `systemd-analyze` su Windows); compileall/shell/diff pass. QEMU fake failure-path verifica exit code e cleanup overlay.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows AMD64 + WSL Debian 13, GCC/QEMU x86_64 presenti; BitBake assente, nessun checkout/fetch Yocto.
- **Git**: firing-start HEAD `23a77ce153a5bfcd347a394c26273d7a3dd4d8b3`; QEMU failure-path guard pubblicato in `57068b0`. `.pi-loop.json` non tracciato, ZIP ignorati.
- **Prossimo**: parse/build su host OE release-pinned quando selezionato; distinguere audit statici da parse/runtime.
