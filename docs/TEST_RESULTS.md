# Risultati test

## 2026-10-18 — Dipendenze runtime Yocto

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test scaffolding.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- Suite completa finale: `python -m unittest discover -s tests -v` — PASS, 43 test.
- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS; `bash -n install.sh setup-ai-cpu.sh` — PASS; `git diff --check` — PASS.
- `bash -n install.sh setup-ai-cpu.sh` — PASS, nessuna modifica agli script.
- Analisi AST dei moduli runtime rileva import standard-library e verifica il mapping package dichiarato nella ricetta.
- BitBake non disponibile; naming/ownership dei package non verificati dal metadata reale della release OE.
