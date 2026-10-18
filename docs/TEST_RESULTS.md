# Risultati test

## 2026-10-18 — Coerenza stati not-built/not-run

- Sample evidence verificato: immagini not-built implicano exit/artifact/hash null; boot not-run implica smoke checks tutti not-run.
- Test mirato Windows — PASS.
- Windows/Python 3.11 suite — PASS, 59 test; WSL Debian 13/Python 3.13 suite — PASS, 59 test.
- Compileall + shell syntax su entrambi — PASS; `git diff --check` — PASS.
- Nessun parse/build reale svolto.
