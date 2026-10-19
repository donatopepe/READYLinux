# Risultati test

## 2026-10-18 — Baseline recipe-source guard

- Snapshot firing iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4a3c4da1e8339070f7a388247340c810bed87332`.
- WSL systemd historical security report: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico verifica firing HEAD, count test e limiti host nei documenti di stato.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi eseguiti: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Applicazione: source `file://` recipe inventory verificato staticamente. Nessun BitBake parse/build, image build o boot QEMU reale.
