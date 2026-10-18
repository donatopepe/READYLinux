# Risultati test

## 2026-10-18 — Hardening servizio console

- Modificato servizio per utente non privilegiato `ready`, `StateDirectory=/var/lib/readylinux`, `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`, `ProtectHome` e sole scritture autorizzate sullo state.
- Ricetta useradd crea gruppo/utente di sistema.
- `python -m unittest discover -s tests -v` — PASS, 43 test; `compileall`, `bash -n` e `git diff --check` — PASS. Test statici verificano User, state persistente e hardening dichiarato.
- BitBake/QEMU non disponibili: nessun parse/build/boot verificato.
