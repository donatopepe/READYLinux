# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root; helper `scripts/validate-yocto-env.sh` esegue preflight e parse-only BitBake.
- **Verificato localmente**: 55 test, compileall, `bash -n`, `git diff --check`; template guard verifica placeholders e dati non compilati.
- **Non verificato**: parse reale OE, build/boot QEMU, package mapping, service boot, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; BitBake assente, nessun download/installazione.
- **Git**: `main` era a `fab3caf`; guard template verificato, publish in corso. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: validazione riproducibile su host Linux con commit OE/layer, distro, MACHINE, build log, checksum immagine e boot QEMU raccolti secondo `meta-readylinux/README.md`.
