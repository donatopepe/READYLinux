# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, scaffolding Yocto, servizio systemd tty1 non-root con hardening; helper validation BitBake/systemd/checksum artifact.
- **Verificato localmente**: 66 test su Windows/MSYS Python 3.11 e WSL Debian 13 Python 3.13; compileall e `bash -n` su entrambi; `git diff --check` pulito. Unit systemd passa `systemd-analyze verify` (copia temporanea, ExecStart sostituito). `systemd-analyze security --offline`: MEDIUM, score exposure 6.7, residuo UMask 0027.
- **Non verificato**: BitBake/Yocto parse/build, boot immagine QEMU, getty mask nell'immagine, comportamento runtime dell'unit, artifact READY reale, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows 10 AMD64 + WSL2 Debian 13; 20 CPU logiche, 30 GiB RAM WSL, GCC e QEMU x86_64 installati. BitBake non disponibile. Nessun checkout/fetch Yocto effettuato.
- **Git**: `main` sincronizzato con `origin/main`; baseline aggiornata nel commit `32cb352`. ZIP e `.pi-loop*` restano non tracciati/esclusi.
- **Prossimo**: scegliere release/BSP e ottenere BitBake su host Linux prima di metadata parse e build; non dichiarare riproducibilità/boot finché checklist README non ha evidenze.
