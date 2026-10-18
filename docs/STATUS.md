# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root con state persistente, hardening systemd e getty tty1 mascherato.
- **Verificato localmente**: 43 test, compileall, `bash -n`, `git diff --check`; test statici coprono ownership tty1 e vincolo seriale differita. BitBake/QEMU assenti.
- **Non verificato**: parse/build/boot Yocto/QEMU, mask getty reale, login/console boot, mapping OE, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Impatto UX**: tty1 riservato a READY, nessun login prompt normale su quel terminale; scelta documentata. Console seriale differita finché non viene scelto BSP/target.
- **Host**: Windows/MSYS AMD64, Python 3.11; niente download/installazioni.
- **Git**: `main` sincronizzato con `origin/main`; selezione console documentata nel commit `9dc4207`. ZIP/loop state esclusi.
- **Prossimo**: scegliere release Yocto + machine/BSP prima di estendere console seriale; nel frattempo completare verifiche locali M2. BitBake su Linux resta non verificato.
