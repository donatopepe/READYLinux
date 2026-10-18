# Risultati test

## 2026-10-18 — Ownership tty1

- Documentato che `getty@tty1.service` è mascherato e tty1 riservato a READY.
- Test statici controllano unità, recipe `FILES`, target multi-user e assenza di login service concorrente.
- `python -m unittest discover -s tests -v` — PASS, 43 test; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake/QEMU non disponibili; nessuna verifica immagine/boot.
