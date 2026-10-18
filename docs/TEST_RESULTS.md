# Risultati test

## 2026-10-18 — Configurazione distro/BSP opt-in

- README build ora indica esplicitamente `DISTRO = "readylinux"` e lascia `MACHINE` come placeholder scelto dall'utente; nessun BSP viene assunto automaticamente.
- Test statico verifica `readylinux.conf` abilita systemd, image recipe non forza la distro, entrambi README danno istruzioni coerenti.
- Test mirato Windows/Python 3.11 e WSL Debian 13/Python 3.13 — PASS.
- Nessun BitBake e nessun BSP selezionato, quindi nessun parse/build reale.

## 2026-10-18 — Baseline test/status

- Nuovo test statico IT/EN per ownership tty1, maschera getty e messaggio assenza login prompt.

- HEAD snapshot a inizio firing: `1e3a456a489b20340ba41f568efe5fa478c9657b`; test statico richiede snapshot e baseline in status IT/EN.
- Full suite Windows/Python 3.11 — PASS, 95 test (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13 — PASS, 95 test.
- `compileall`, shell syntax su entrambi e `git diff --check` — PASS.

## 2026-10-18 — Documentazione package ownership

- Test statico aggiunto: unit e recipe devono assegnare `/dev/tty1` a READY, mascherare `getty@tty1.service`, e entrambi i README spiegano terminale riservato senza login prompt.
- User/group/state test verifica che unit `User`/`Group` e `StateDirectory=readylinux` corrispondano a USERADD/GROUPADD, path persistente e mode 0750.
- Writable-state scope test: `StateDirectory=readylinux`, `ReadWritePaths=/var/lib/readylinux`, XDG state path allineati; broad writable paths rifiutati.
- Test statico aggiunto che `StateDirectory`, `ReadWritePaths` e `XDG_DATA_HOME` restino allineati su `/var/lib/readylinux`, senza writable paths broad (`/home`, `/etc`, `/usr`, `/opt`).
- Test statico aggiunto: direttive hardening dell'unit systemd richieste e claim README IT/EN coerenti.
- Image recipe audit: LICENSE=MIT, core-image-minimal base, IMAGE_INSTALL exactly runtime+console, no external URI/model references; distro policy enables systemd.
- Image inclusion audit statico verifica che `IMAGE_INSTALL:append` contenga una sola volta ogni custom recipe package (runtime + console).
- Full-suite command: `python -m unittest discover -s tests -v`; compileall and `bash -n` are also run in platform verification.
- README layer IT/EN ora specificano che unità systemd e getty mask appartengono a `readylinux-console`, installato nella image recipe.
- Test statico confronta tali istruzioni con `RDEPENDS`, `FILES:${PN}` e symlink installati; image inclusion audit verifica che runtime/console siano inclusi una volta in `IMAGE_INSTALL`.
- Finding hardening systemd precedente: `systemd-analyze security --offline`, `MEDIUM/6.7`, `UMask 0027`.
- Windows/Python 3.11 full suite — PASS, 92 test (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13 full suite — PASS, 92 test.
- Compileall, shell syntax su entrambi e `git diff --check` — PASS.
- Nessun BitBake/package QA disponibile; nessun QEMU boot reale.
