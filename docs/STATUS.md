# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio tty1 hardenizzato; helper host preflight, BitBake, systemd, checksum artifact e boot QEMU isolato con overlay COW.
- **Verificato localmente**: 78 test su Windows/Python 3.11 (1 skip previsto) e WSL Debian 13/Python 3.13; compileall/shell syntax/diff check pass. systemd verify/security MEDIUM/6.7; fake QEMU COW cleanup pass.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine READY QEMU, getty mask nell'immagine, comportamento unit reale, hash artifact READY, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13, QEMU x86_64 e GCC installati; BitBake assente, nessun checkout/fetch Yocto. Probe host read-only disponibile.
- **Git**: `main` sincronizzato con `origin/main` a `8a287643b5498a307ee8b41e70c85277fcb1b1b0`; ZIP e `.pi-loop*` restano non tracciati/esclusi.
- **Prossimo**: scegliere release/BSP e predisporre BitBake prima di parse/build; seguire acceptance checklist README, non dichiarare boot/reproducibilità prima delle evidenze.
