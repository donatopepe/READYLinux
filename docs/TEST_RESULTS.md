# Risultati test

## 2026-10-18 — Criteri evidenza build Yocto

- Guide IT/EN definiscono prerequisiti per dichiarare build riproducibile: commit OE/layer, distro/MACHINE, versione BitBake, log parse/build, checksum artifact, boot QEMU/controlli tty/state.
- Test statico bilingual verifica presenza checklist.
- `python -m unittest discover -s tests -v` — PASS, 53 test.
- compileall, `bash -n`, `git diff --check` — PASS.
- Build e boot non eseguiti (BitBake/QEMU assenti).


## 2026-10-18 — Wiring image/package Yocto

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test.
- Test controlla package `IMAGE_INSTALL` esattamente, recipe presenti e `RDEPENDS` del servizio console su `readylinux systemd`.
- `python -m unittest discover -s tests -v` — PASS, 52 test; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake non disponibile; package resolution metadata reale non testata.
