# Risultati test

## 2026-10-18 — Baseline verificata al firing

- License checksum audit verifica che le due recipe MIT usino lo stesso `LIC_FILES_CHKSUM` e il digest atteso.
- Runtime dependency closure verifica import stdlib -> `RDEPENDS` e inclusion dei package in `IMAGE_INSTALL`.
- SRC_URI extractor statico include fixture URI options (`;apply=yes`, `;unpack=0`) e verifica basename corretti; nessuna fetch eseguita.
- Full-suite command: `python -m unittest discover -s tests -v`.
- Snapshot d'inizio: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json` non tracciato; HEAD `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`.
- Osservazione WSL precedente `systemd-analyze security --offline`: MEDIUM/6.7, UMask 0027.
- Status IT/EN aggiornati a HEAD firing `ed2489483479fbc86b4f49b64b6dd85c55f4c48d`; test statico controlla hash, baseline e limiti host.
- Windows/Python 3.11: 98 test PASS (1 skip `systemd-analyze`); WSL Debian 13/Python 3.13: 98 test PASS.
- Comandi verificati: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`, `bash -n` scripts e `git diff --check` superati su entrambi.
- BitBake/Yocto parse/build e boot QEMU reali non eseguiti.
