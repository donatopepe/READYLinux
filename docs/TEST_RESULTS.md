# Risultati test

## 2026-10-18 — Stato parse nel sample evidence

- `parse_exit_code` reso nullable; sample `NOT-RUN` non dichiara più exit 0 fuorviante.
- Test verifica log NOT-RUN e exit null nel sample.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
- Nessun parse reale effettuato.
