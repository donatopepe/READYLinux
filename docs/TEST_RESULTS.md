# Risultati test

## 2026-10-18 — Documentazione package ownership

- Writable-state scope test: `StateDirectory=readylinux`, `ReadWritePaths=/var/lib/readylinux`, XDG state path allineati; broad writable paths rifiutati.
- Test statico aggiunto che `StateDirectory`, `ReadWritePaths` e `XDG_DATA_HOME` restino allineati su `/var/lib/readylinux`, senza writable paths broad (`/home`, `/etc`, `/usr`, `/opt`).
- Test statico aggiunto: direttive hardening dell'unit systemd richieste e claim README IT/EN coerenti.
- Image recipe audit: LICENSE=MIT, core-image-minimal base, IMAGE_INSTALL exactly runtime+console, no external URI/model references; distro policy enables systemd.
- Image inclusion audit statico verifica che `IMAGE_INSTALL:append` contenga una sola volta ogni custom recipe package (runtime + console).
- Full-suite command: `python -m unittest discover -s tests -v`; compileall and `bash -n` are also run in platform verification.
- README layer IT/EN ora specificano che unità systemd e getty mask appartengono a `readylinux-console`, installato nella image recipe.
- Test statico confronta tali istruzioni con `RDEPENDS`, `FILES:${PN}` e symlink installati; image inclusion audit verifica che runtime/console siano inclusi una volta in `IMAGE_INSTALL`.
- Finding hardening systemd precedente: `systemd-analyze security --offline`, `MEDIUM/6.7`, `UMask 0027`.
- Windows/Python 3.11 full suite — PASS, 91 test (1 skip systemd-analyze); WSL Debian 13/Python 3.13 full suite — PASS, 91 test.
- Compileall, shell syntax su entrambi e `git diff --check` — PASS.
- Nessun BitBake/package QA disponibile; nessun QEMU boot reale.
