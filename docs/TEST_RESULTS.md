# Risultati test

## 2026-10-18 — Scaffolding Yocto M2

- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 42 test.
- `bash -n install.sh setup-ai-cpu.sh` — PASS.
- Test statici verificano metadati layer, sorgenti locali ricetta, immagine, unità systemd tty1 abilitata e assenza di URI fetch esterni.
- BitBake non disponibile su Windows/MSYS: nessun parse BitBake, build immagine o boot QEMU eseguiti.

## 2026-10-18 — Runtime BASIC M1 (in corso)

- `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 37 test (26 baseline + 11 BASIC).
- `bash -n install.sh setup-ai-cpu.sh` — PASS.
- BASIC verificato: output/arithmetic, IF/GOTO, FOR/NEXT, INPUT, GOSUB/RETURN, edit/delete/list, save/load via console, rejection di chiamate Python e istruzioni sconosciute, step limit.
- Non coperti da suite: boot Yocto/QEMU, inferenza GGUF reale, sandbox codice generato.
- Questo non verifica Commodore BASIC completo, sandbox codice generato o OS embedded.


## 2026-10-18 — Baseline

Ambiente Windows 10 AMD64, Python 3.11.7.

- `python -m compileall -q readylinux.py ai_local.py vibe.py` — PASS.
- `python -m unittest discover -s tests -v` — PASS, 26 test.
- `bash -n install.sh setup-ai-cpu.sh` — PASS in Bash/MSYS.

I test HTTP simulano il server AI: nessuna inferenza reale testata. Nessun test QEMU, kernel, Yocto, GPU o sandbox.
