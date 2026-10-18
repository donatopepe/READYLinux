# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto e servizio tty1 non-root con state persistente, hardening systemd e getty tty1 mascherato.
- **Verificato localmente**: 43 test, compileall, `bash -n`, `git diff --check`; test statici coprono ownership tty1 e packaging unità. BitBake/QEMU assenti.
- **Non verificato**: parse/build/boot Yocto/QEMU, mask getty reale, login/console boot, mapping OE, kernel, GGUF reale, sandbox, GPU, ARM64, benchmark.
- **Impatto UX**: tty1 riservato a READY, nessun login prompt normale su quel terminale; scelta documentata.
- **Host**: Windows/MSYS AMD64, Python 3.11; niente download/installazioni.
- **Git**: `main` a `0165f09` all'avvio; modifiche ownership tty1 testate, commit/push in corso. ZIP/loop state esclusi.
- **Prossimo**: eseguire suite, poi migliorare modalità diagnostica/console seriale con target esplicito; BitBake su Linux resta non verificato.
