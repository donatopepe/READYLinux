# Baseline READY Linux

Data rilevazione: 2026-10-18. Sorgente baseline: archivio `READYLinux_0.3_Codex_Handoff.zip`, estratto nella root.

## Prodotto verificato

- READY 0.3 è un'applicazione terminale Python, non una distribuzione Linux né un desktop.
- Programmazione numerata implementata in Python; non è Commodore BASIC e non ha parser BASIC.
- Flusso vibe coding con AI locale opzionale, proposta JSON, diff, approvazione, verifiche statiche ed esecuzione esplicita.
- `vibe.py` contiene workspace e gestione proposte; `ai_local.py` usa llama-server locale.
- Inferenza GGUF reale, sandbox, immagine bootabile e GUI non sono verificate/implementate.

## Ambiente di verifica

- Host: Windows 10, architettura AMD64; Python 3.11.7; 20 processori logici riportati da Python.
- Disponibili: Git 2.49.0, Node, Pi CLI.
- Non trovati nel PATH: BitBake, QEMU x86-64/ARM64, Docker/Podman, Clang, GCC.
- Memoria RAM non rilevata: `free` non disponibile nell'ambiente MSYS.

## Baseline test

- `python -m compileall -q readylinux.py ai_local.py vibe.py`: pass
- `python -m unittest discover -s tests -v`: 26 test pass
- `bash -n install.sh setup-ai-cpu.sh`: pass
- Test AI usano HTTP simulato; non provano inferenza reale.

## Repository

- Git root: repository READY Linux. Branch `main`, remote `origin` configurato su `https://github.com/donatopepe/READYLinux.git`.
- Nessun commit ancora. Archivi ZIP sono input sorgente e non devono entrare nel runtime.
