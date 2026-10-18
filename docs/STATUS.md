# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root; helper `scripts/validate-yocto-env.sh` esegue preflight e parse-only BitBake.
- **Verificato localmente**: 52 test, compileall, `bash -n`, `git diff --check`; regressioni hardening service/write path testate staticamente. BitBake assente.
- **Non verificato**: parse reale OE, build/boot QEMU, package mapping, service boot, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11; BitBake assente, nessun download/installazione.
- **Git**: `main` era a `0c51ba5` all'avvio unità; test regressioni sicurezza in verifica. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: test suite e publish; poi bitbake parse su host OE configurato.
