# Risultati test

## 2026-10-18 — Selezione console

- Decisione documentata: scaffold generico usa tty1, seriale rinviata finché non viene scelto BSP/machine; nomi device e policy login dipendono dal target.
- Test statici verificano il vincolo documentale.
- `python -m unittest discover -s tests -v` — PASS, 43 test; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake/QEMU non disponibili.
