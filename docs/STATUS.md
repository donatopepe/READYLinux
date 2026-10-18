# Stato READY Linux

Aggiornato: 2026-10-18.

- **Release**: READY Linux 0.3, prototipo applicativo.
- **Implementato**: console, vibe/BASIC, Yocto scaffold e servizio tty1 non-root hardenizzato; helper validation BitBake/systemd/image SHA.
- **Verificato**: 66 test PASS su Windows e WSL; WSL systemd-analyze verify PASS; security report MEDIUM exposure (UMask 0027, file group-readable). Hardening assertions aggiornate.
- **Non verificato**: BitBake/image build, QEMU boot, getty mask dentro image, service runtime target, model/sandbox/GPU/ARM64.
- **Host**: Windows+WSL Debian 13, QEMU x86_64 installato; BitBake assente. Nessun checkout sorgenti Yocto.
- **Git**: `main` sincronizzato con `origin/main`; hardening unit systemd pubblicato in `0eb8552`. ZIP/`.pi-loop*` esclusi.
- **Prossimo**: eseguire test cross-platform, documentare exposure metric e pubblicare.
