# Risultati test

## 2026-10-18 — Launcher Yocto

- Corretto launcher installato: heredoc quoted non espande variabili BitBake; percorso runtime reso statico `/usr/share/readylinux/readylinux.py`.
- Test mirato: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test.
- Suite completa finale: `python -m unittest discover -s tests -v` — PASS, 43 test; `compileall`, `bash -n` e `git diff --check` — PASS.
- BitBake assente; package/image non buildati.
