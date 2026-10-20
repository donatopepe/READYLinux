# Risultati test

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
