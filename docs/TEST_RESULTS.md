# Risultati test

## 2026-10-18 — Chiarezza sample manifest

- Il test verifica `run_id` example, host/MACHINE/version non registrati, parse NOT-RUN, `deviations` esplicita e verdict not-verified.
- Test mirato schema/sample: PASS.
- `python -m unittest discover -s tests -v` — PASS, 58 test; compileall, `bash -n`, `git diff --check` — PASS.
- Il record resta dimostrativo; nessun risultato reale inserito.
