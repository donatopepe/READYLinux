# Risultati test

## 2026-10-20 — Parità documentazione BASIC ↔ implementazione

- Nuovo modulo `tests/test_basic_docs.py` (5 test): confronta i keyword rivendicati nei due documenti IT/EN, verifica che ogni keyword del linguaggio esista in `basic.py`, che i comandi console (`LIST`, `RUN`, `NEW`, `HELP`, `STOP`, `SAVE`, `LOAD`, `EDIT`) esistano in `readylinux.py`, e che entrambi i documenti mantengano il disclaimer "non piena compatibilità Commodore" e l'avviso "questa restrizione non è una sandbox".
- Bug trovato nei test stessi durante il firing: `RUN` è un comando console, non un keyword del linguaggio → l'estrazione è stata limitata alla riga "## Linguaggio implementato"; la regex italiana sulla sandbox conteneva un carattere accentato interpretato male → sostituita con `non.{0,20}una sandbox`.
- Suite: 225 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Roadmap M1 allineata a console e BASIC reali

- `docs/ROADMAP.en.md` M1 affermava ancora: "standalone `basic.py` plus 9 focused tests; console integration, persistence commands, bilingual user docs, and full green suite remain incomplete". Tutte e quattro le affermazioni erano false: `readylinux.py` integra `BasicProgram` con `SAVE`/`LOAD`, esistono `docs/BASIC.md` e `docs/BASIC.en.md`, i test BASIC sono 11 e la suite è verde.
- Testo EN riscritto in parità con l'IT: implementazione ridotta con test, integrazione console con persistenza, documentazione bilingue, suite verde, compatibilità Commodore completa non dichiarata.
- Nuovo test `test_roadmap_m1_claims_match_console_and_basic_reality`: richiede `BasicProgram`/`SAVE`/`LOAD` nel console, i due documenti BASIC, e vieta il ritorno di "remain incomplete" o l'assenza del caveat.
- Suite: 220 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Serie OE registrata nell'evidenza build

- Lo schema `docs/YOCTO_BUILD_EVIDENCE.schema.json` richiede ora `identity.oe_series`, allineato al gate del validatore che legge `LAYERSERIES_COMPAT_core`: un record di build non può più omettere la serie OE su cui è stato prodotto.
- Esempio aggiornato con il placeholder `"oe_series": "UNVERIFIED"`; template IT/EN riportano la riga "OE release series (from `LAYERSERIES_COMPAT_core`, e.g. scarthgap)".
- Nuovo test `test_build_evidence_records_the_oe_release_series` verifica campo obbligatorio, placeholder dell'esempio e presenza della riga nei due template.
- Suite: 219 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Verifica offline di record di evidenza esistenti

- `scripts/record-yocto-preflight.py --check PATH` valida un record già scritto contro le stesse regole del recorder: chiavi esatte (nessuna mancante o extra), `schema_version=1`, `recorded_utc` in forma UTC, commit 40 hex, `scope` che dichiari "not build evidence", `preflight_exit_code=0`, struttura di `preflight` (os/arch/cpus/required/optional/builddir/verdict) e coerenza `ready` ⇒ builddir impostata e `missing_required` vuoto. Exit 0 valido, 8 invalido (anche JSON rotto o file assente).
- L'esempio documentato `docs/YOCTO_PREFLIGHT_RECORD.example.json` passa la validazione; cinque nuovi test coprono esempio valido, `ready` senza builddir, chiavi mancanti/extra, scope ingannevole, JSON rotto e file assente.
- Suite: 218 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Roadmap e README layer allineati al parse verificato

- `meta-readylinux/README.md` e `README.en.md` affermavano che **nessuna** serie era verificata: ora dichiarano scarthgap verificato su Poky pinnato `104772c5fd06…` con `bitbake -p` a 0 errori, e lasciano styhead/walnascar/wrynose esplicitamente non verificate.
- `docs/ROADMAP.md` / `ROADMAP.en.md` M2 riportavano "parse non verificato" e la tally obsoleta `19/19`: aggiornati con parse verificato, 24 comandi host, `lz4c` shim, `bitbake -n` 5006 task e lista aggiornata dei residui (build `.wic`, boot, guest SSH, getty mask, MACHINE).
- Test aggiornati: la regex sul claim di verifica accetta sia "has" sia "have"; nuovo `test_roadmap_states_parse_verified_and_build_unverified` vieta il ritorno di `19/19` e richiede il commit pinnato e la menzione `.wic`.
- Suite: 213 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Punteggio systemd misurabile e gate sulla soglia

- `scripts/validate-systemd-unit.sh` accetta `--security`: esegue `systemd-analyze security --offline=yes` sulla copia temporanea con `ExecStart` sostituito, estrae il punteggio e fallisce con **exit 7** se supera `READY_MAX_EXPOSURE` (default `8.0`). Argomenti ignoti → exit 64.
- Run reale su WSL Debian 13 (systemd 257): `Exposure level: 6.7 (limit 8.0)`, exit 0 — il valore MEDIUM/6.7 non è più solo storico nei documenti, è riproducibile con un comando.
- Test: modulo systemd da 4 a 8 casi — stub `systemd-analyze` per 9.5 (exit 7) e 4.2 (exit 0), run reale con `--security`, argomento ignoto (exit 64).
- Suite: 212 test PASS (26 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Contratto artefatto verificato nel validatore

- `scripts/validate-yocto-env.sh`, dopo `bitbake -p`, interroga `bitbake-getvar --recipe readylinux-image --value IMAGE_FSTYPES`; se `wic` non è presente esce con **6** e non dichiara l'ambiente valido. Se `bitbake-getvar` manca stampa un NOTE non fatale.
- Run reale su WSL/Poky scarthgap: `Image fstypes:  tar.bz2 ext4 wic`, exit 0.
- Test: stub `bitbake-getvar` nell'helper; due nuovi casi (`tar.bz2 ext4` → exit 6; `ext4 wic` → exit 0 con stampa). Modulo validatore: 19 test.
- Suite: 208 test PASS (23 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Artefatto `.wic` coerente con la documentazione

- La documentazione e gli helper `verify-image-artifact.sh` / `boot-image-qemu.sh` consumano un `.wic`, ma la image recipe non impostava `IMAGE_FSTYPES`: il default di `core-image-minimal` è `tar.bz2 ext4`, quindi il file documentato non sarebbe mai stato prodotto.
- Fix: `IMAGE_FSTYPES:append = " wic"` in `readylinux-image.bb`, con commento sul perché.
- Verifica offline con `bitbake -e readylinux-image` (nessun fetch): `IMAGE_FSTYPES=" tar.bz2 ext4 wic"`, `IMAGE_INSTALL="packagegroup-core-boot  readylinux-runtime readylinux-console"`.
- Nuovo test `test_image_recipe_produces_the_documented_wic_artifact`: una sola assegnazione `IMAGE_FSTYPES`, presenza di `wic`, e README IT/EN che citano `.wic` e `IMAGE_FSTYPES`.
- Suite: 206 test PASS (21 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Compatibilità serie OE verificata prima del parse

- `scripts/validate-yocto-env.sh` legge `LAYERSERIES_COMPAT_core` dal `conf/layer.conf` del layer `core` riportato da `bitbake-layers show-layers` e lo confronta con `LAYERSERIES_COMPAT_readylinux`: se non c'è intersezione esce con 5 e non lancia il parse; se il layer `core` o il suo `layer.conf` non sono leggibili esce con 4.
- Run reale su WSL/Poky scarthgap: `Layer collection: readylinux (priority 8)` + `OE series: scarthgap`, poi `bitbake -p` senza errori.
- Test: helper aggiornato con layer `core` sintetico; due nuovi casi (serie compatibile → stampa `OE series: styhead`; serie `kirkstone` non elencata → exit 5). Modulo validatore: 17 test.
- Suite: 205 test PASS (21 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Gate di registrazione layer prima del parse

- `scripts/validate-yocto-env.sh` ora interroga `bitbake-layers show-layers`: richiede che il path del layer compaia nel report, che la collection sia `readylinux` e che la priority sia numerica; altrimenti exit 4. Se `bitbake-layers` manca, exit 2.
- Run reale su WSL: `Layer collection: readylinux (priority 8)` seguito da `bitbake -p` con 0 errori.
- Test: helper aggiornato con stub `bitbake-layers`; due nuovi casi (collection errata → exit 4; report con path diverso → exit 4). Totale modulo 15 test.
- Suite: 203 test PASS (19 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Test degli installer utente (`install.sh`, `setup-ai-cpu.sh`)

- Nuovo modulo `tests/test_install_script.py` (5 test) per i due script finora coperti solo dalla sintassi.
- `install.sh`: verifica esecuzione reale con `HOME`/`XDG_DATA_HOME` temporanei — copia `readylinux.py`, `ai_local.py`, `vibe.py` in `$XDG_DATA_HOME/readylinux/app`, crea il wrapper eseguibile in `$HOME/.local/bin` con shebang bash e path assoluto dell'app, nessun file creato fuori dalla home; verifica fail-closed con `python3` assente (exit 1).
- `setup-ai-cpu.sh`: verifica opt-in CPU-only, SHA-256 del modello pinnato `cc324af0…`, uso di `sha256sum -c`, nessun `sudo`/`systemctl`, e fail-closed (exit 1, nessun file) quando mancano i tool.
- Bug trovato nei test stessi: con `PATH` svuotato l'invocazione di `bash` falliva su WSL (risolto usando il path assoluto su POSIX, `bash` su Windows).
- Suite: 201 test PASS (17 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Verification plan riallineato all'evidenza reale

- `docs/VERIFICATION_PLAN.md` affermava ancora "nessun download consentito", "19/19 comandi" e "non dichiarare che la layer parsa": tutto superato dai fatti. Aggiornato con: Poky pinnato `104772c5fd0653290cbb5e4b77813343957939cc`, `BUILDDIR=~/yocto/build`, parse `0 errors`, fix `readylinux-runtime` e `usrmerge`, 24 comandi host, shim `lz4c`, `bitbake -n readylinux-image` 5006 task noexec.
- Nuovo guard `test_verification_plan_records_the_pinned_parse_evidence` impedisce che il piano torni a dichiarare il parse non eseguito o a citare 19 comandi.
- Suite: 196 test PASS (17 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Preflight esteso: `lz4c` e tool BitBake reali

- `bitbake` in scarthgap richiede `lz4c`, assente in Debian 13: il probe con 19 comandi dichiarava `ready` mentre BitBake falliva con `HOSTTOOLS ... lz4c unavailable`. Falso positivo reale.
- `required_commands` esteso da 19 a 24: aggiunti `lz4c`, `patch`, `perl`, `tar`, `xargs` (presenti in `HOSTTOOLS` di `meta/conf/bitbake.conf`).
- Sul PATH di sistema: `MISSING lz4c` → `INCOMPLETE` (comportamento corretto). Con `~/yocto/hosttools` su `PATH`: 24/24 `OK`, `bitbake` `FOUND`, `BUILDDIR=~/yocto/build`.
- Evidenza reale registrata: `python3 scripts/record-yocto-preflight.py …` → `verdict: ready`, `readylinux_commit: 13800fdd…`, `recorded_utc: 2026-10-20T20:36:37Z`, `missing_required: []`, `builddir.set: true`.
- Suite: 195 test PASS (17 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.

## 2026-10-20 — Fix distro feature `usrmerge` e grafo immagine (noexec)

- Verifica recipe con `bitbake -e` (nessun fetch/build): `readylinux-runtime` risolve `PN=readylinux-runtime`, `PV=0.3`, `RDEPENDS` package-specific e `FILES` con `/usr/share/readylinux` e `/usr/bin/readylinux`.
- `bitbake -e readylinux-console` **falliva**: `ERROR: Nothing RPROVIDES 'systemd' ... systemd was skipped: missing required distro feature 'usrmerge'`. Il parse da solo non lo rilevava.
- Fix: `DISTRO_FEATURES:append = " systemd usrmerge"` in `conf/distro/readylinux.conf`; test aggiornati per richiedere `usrmerge`.
- Dopo il fix: `bitbake -e readylinux-console` → `RDEPENDS:readylinux-console=" readylinux-runtime systemd"`, `FILES` include unit e mask, `SYSTEMD_SERVICE`/`SYSTEMD_AUTO_ENABLE` corretti.
- `bitbake -n readylinux-image` (dry run, nessuna esecuzione né fetch): `Attempted 5006 tasks ... all succeeded`, incluso `readylinux-image.bb:do_build`. Un warning: Debian 13 non validato da OE.
- Suite: 195 test PASS (17 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.
- Restano non verificati: build immagine reale (richiede fetch sorgenti), boot QEMU, guest SSH, getty mask nell'immagine, hash artifact.

## 2026-10-20 — Primo parse BitBake reale (Poky scarthgap pinnato)

- Host: WSL Debian 13, utente non privilegiato. Comandi: `bash scripts/check-yocto-host.sh` (19/19 `OK`, `qemu` trovato, `bitbake` assente, `BUILDDIR` unset prima del provisioning).
- Provisioning locale senza root: `git fetch --depth 1` del commit Poky `104772c5fd0653290cbb5e4b77813343957939cc` (scarthgap) in `~/yocto/poky-src`; `lz4c` mancante risolto con `apt-get download lz4` + `dpkg -x` in `~/yocto/hosttools` (nessun `sudo`, nessuna installazione di sistema).
- `source oe-init-build-env ~/yocto/build` + `bitbake-layers add-layer /mnt/d/repos/ReadyLinux/meta-readylinux` + `DISTRO = "readylinux"` in `local.conf`.
- Primo `bash scripts/validate-yocto-env.sh`: **fallito** con 5 errori QA reali della recipe runtime — `pn-overrides` (PN `readylinux` collidente con la distro) e `pkgvarcheck` su `RDEPENDS`/`FILES` non package-specific.
- Fix: recipe rinominata `readylinux-runtime_0.3.bb`, `IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"`, `RDEPENDS` della console su `readylinux-runtime`.
- Secondo run: `Parsing of 923 .bb files complete (503 cached, 420 parsed). 1881 targets, 49 skipped, 0 masked, 0 errors.` exit 0; unico warning: Debian 13 non validato da OE.
- Suite completa dopo il rename: 195 test PASS (17 skip su Windows) su Windows/Python 3.11 e WSL Debian 13/Python 3.13.
- Restano non verificati: build immagine, boot QEMU, guest SSH, getty mask nell'immagine, hash artifact.

## 2026-10-20 — Correzione evidenza preflight e baseline 174

- Il probe `bash scripts/check-yocto-host.sh` eseguito dalla shell Windows (Git Bash) non è un host Debian: riporta `/etc/os-release` assente e tool mancanti. Quell'output non è evidenza Yocto e non va registrato.
- Comando corretto, eseguito dentro WSL Debian 13: `wsl -d Debian -- /bin/bash -c 'cd /mnt/d/repos/ReadyLinux && /bin/bash scripts/check-yocto-host.sh'`; exit 1 `INCOMPLETE`, 19/19 comandi host richiesti `OK`, `qemu-system-x86_64` e `sha256sum` trovati, `bitbake`/`bitbake-layers` assenti, `BUILDDIR` unset.
- Aggiunto un test che impone agli STATUS IT/EN di riportare il risultato WSL Debian e vieta di registrare l'output della shell Windows come evidenza host.
- Suite completa: 179 test PASS (10 skip platform-specific) su Windows/Python 3.11 e WSL Debian 13/Python 3.13; `compileall`, `bash -n` e `git diff --check` pass.
- Nessun download, installazione, parse BitBake, build immagine o boot QEMU eseguito.
- Nuovo `scripts/record-yocto-preflight.py`: registra il report `--json` con commit/UTC e scope "preflight-only, non build evidence"; rifiuta di scrivere se il verdetto non è `ready` (exit 3) o se il file esiste senza `--force` (exit 4). Suite: 184 test PASS (13 skip su Windows).
- Aggiunto schema `docs/YOCTO_PREFLIGHT_RECORD.schema.json` + esempio placeholder e test su struttura del record e output del recorder; il verdetto `ready` deve essere coerente con builddir e BitBake. Suite: 188 test PASS (14 skip su Windows).
- `scripts/check-yocto-host.sh` ora è fail-closed sull'ambiente: senza `/etc/os-release` leggibile termina con exit 2 `NOT-A-LINUX-HOST` e `WRONG-ENVIRONMENT`, perché l'output di una shell Windows non è evidenza host. Exit 0 = pronto, 1 = `INCOMPLETE`, 2 = ambiente sbagliato. Suite: 175 test PASS.

- Recorder più severo: un report che si dichiara `ready` con `missing_required` non vuoto o `builddir` non impostata viene rifiutato (exit 5) senza scrivere nulla; aggiunti 2 test. Suite: 190 test PASS (14 skip su Windows).

- Script tracker: tutti gli `install.sh`, `setup-ai-cpu.sh`, `scripts/*.sh` e `scripts/*.py` erano committati `100644` (non eseguibili); ripristinato `100755` con `git update-index --chmod=+x` e aggiunto guard `test_tracked_scripts_keep_the_executable_bit`. Suite: 191 test PASS (14 skip su Windows).

- Parità README layer: nuovo test confronta i blocchi di comandi IT/EN, i riferimenti `scripts/*.sh|py` e verifica che ogni script citato esista. Suite: 192 test PASS.

- Gate pre-parse: `scripts/validate-yocto-env.sh` ora rifiuta `DISTRO` diverso da `readylinux` (exit 3) e stampa un NOTE se `local.conf` non imposta `DISTRO`; 3 test dedicati. Suite: 195 test PASS (17 skip su Windows).

## 2026-10-18 — Offline Yocto contracts and regression suite

- Runtime recipe test asserts `inherit allarch`, repo-local `file://` app sources, no model/network payload, and declared Python dependencies. Distro static contract also checks that systemd is appended without removing inherited features and selected as init manager.
- Storico WSL systemd security: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static contracts cover layer metadata and unverified compatibility claims; local recipe sources, package closure and launcher-to-service ExecStart path; getty-mask symlink ownership/image inclusion; READY home, persistent StateDirectory and UMask; plus preflight evidence.
- Relevant regressions pass; full suite: 126 tests PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- No BitBake metadata parse, image build or QEMU boot: host lacks BitBake/OE checkout and `BUILDDIR`; no install/download performed.

## 2026-10-18 — Firing-start snapshot and host probe

- Snapshot iniziale verificato con `git rev-parse HEAD`: `92abaae72d9023bb82718ff48e0918ebc17f4b23`; `git status --short --branch` = `main...origin/main`, `.pi-loop.json` e `raw` (0 byte) non tracciati.
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
