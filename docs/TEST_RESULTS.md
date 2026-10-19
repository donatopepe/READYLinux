# Risultati test

## 2026-10-18 — Baseline verificata al firing

- Suite command: `python -m unittest discover -s tests -v`.
- Snapshot iniziale: `git status --short --branch` indicava `main...origin/main`; HEAD `95647fd277c41e20357b01c278e9dd9de7440a1c`; `.pi-loop.json` non tracciato.
- Finding systemd precedente: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN riallineati allo snapshot iniziale; test statico protegge snapshot, conteggio e limiti host.
- Windows/Python 3.11: 98 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 98 test PASS.
- Verifiche: `python -m compileall`; `bash -n` scripts; `git diff --check` passano su entrambi.
- License checksum statico, import-to-RDEPENDS closure, IMAGE_INSTALL closure e SRC_URI options coperte da test.
- User license audit test command: `python -m unittest tests.test_yocto_scaffold.YoctoScaffoldTests.test_license_checksum_is_consistent_across_local_recipes -v`.
- BitBake/Yocto parse/build e boot QEMU reale non eseguiti.
