# Risultati test

## 2026-10-18 — Consistenza status/report e evidenze correnti

- Snapshot iniziale verificato: `git status --short --branch` mostrava `main...origin/main`; HEAD `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`.
- Status IT/EN sono allineati a quello snapshot e distinguono i commit successivi di sola documentazione.
- Comandi standard: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` per gli script shell elencati di seguito.
- Limiti: BitBake/Yocto parse, build immagine e boot QEMU reali non eseguiti.
- Baseline precedente al test nuovo: 78 test Windows (1 skip atteso) e 78 WSL; suite aggiornata da rieseguire.
