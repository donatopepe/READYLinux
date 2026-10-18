# Risultati test

## 2026-10-18 — Esempio JSON schema safety

- Rafforzati controlli stdlib per pattern commit/checksum, enum, nullable exit/artifact, stati non-build/non-boot.
- Il JSON è un esempio con placeholder, non prova di build; schema comment avverte che hash zero/NOT-RUN non sono evidenze.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
