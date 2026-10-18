# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root; helper `scripts/validate-yocto-env.sh` esegue preflight e parse-only BitBake.
- **Verificato localmente**: 58 test, compileall, `bash -n`, `git diff --check`; schema/example coherence pass. Example resta non-verified/non-built.
- **Non verificato**: parse reale OE, build/boot QEMU, package mapping, service boot, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; BitBake assente, nessun download/installazione.
- **Git**: `main` sincronizzato con `origin/main`; esempio non-built pubblicato in `5ff8482`. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: validazione riproducibile su host Linux con commit OE/layer, distro, MACHINE, build log, checksum immagine e boot QEMU raccolti secondo `meta-readylinux/README.md`.
