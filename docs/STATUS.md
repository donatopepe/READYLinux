# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root; helper `scripts/validate-yocto-env.sh` esegue preflight e parse-only BitBake.
- **Verificato localmente**: 58 test, compileall, `bash -n`, `git diff --check`; example manifest non-verified/placeholder esplicito.
- **Non verificato**: parse reale OE, build/boot QEMU, package mapping, service boot, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; BitBake assente, nessun download/installazione.
- **Git**: `main` sincronizzato con `origin/main`; sample placeholder guard pubblicato in `734391c`. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: validazione riproducibile su host Linux con commit OE/layer, distro, MACHINE, build log, checksum immagine e boot QEMU raccolti secondo `meta-readylinux/README.md`.
