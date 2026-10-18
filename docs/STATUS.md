# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3 prototipo applicativo.
- **Implementato**: console Python, vibe flow, BASIC ridotto, layer Yocto, servizio tty1 non-root con hardening e getty mask; script locale `scripts/validate-yocto-env.sh` controlla ambiente già inizializzato e lancia solo `bitbake -p`.
- **Verificato localmente**: 46 test, compileall, sintassi shell e `git diff --check` passati. Helper senza `BUILDDIR` ritorna exit 2 come previsto.
- **Non verificato**: BitBake parse nel vero OE env, image build/boot QEMU, mask getty reale, mapping package, kernel, GGUF, sandbox, GPU/ARM64/benchmark.
- **Host**: Windows/MSYS AMD64, Python 3.11, BitBake assente; niente download/installazioni.
- **Git**: `main` sincronizzato con `origin/main`; helper pubblicato nel commit `b43586a`. ZIP e `.pi-loop*` esclusi.
- **Prossimo**: suite completa e pubblicazione; poi validare metadata in host Linux preconfigurato.
