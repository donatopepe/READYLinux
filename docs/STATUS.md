# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root; helper `scripts/validate-yocto-env.sh` esegue preflight e parse-only BitBake.
- **Verificato localmente**: 59 test, compileall, `bash -n`, `git diff --check`; policy append-only/run ID nei template testata IT/EN.
- **Non verificato**: parse reale OE, build/boot QEMU, package mapping, service boot, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; nessun download/installazione.
- **Git**: `main` era a `39efff6`; policy storico evidenze testata, publish in corso. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: suite completa e pubblicazione; build/boot reale richiede host Linux + OE/QEMU configurati.
