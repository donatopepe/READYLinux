# Risultati test

## 2026-10-18 — Parità template evidenze IT/EN

- Test mirato: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 10 test.
- Assertion verifica corrispondenza dei campi semantici provenance, macchina, config, parse/build, artifact, QEMU, tty, persistenza, BASIC/offline.
- `python -m unittest discover -s tests -v` — PASS, 56 test; compileall, `bash -n`, `git diff --check` — PASS.
- Nessuna build/boot reale (BitBake/QEMU non disponibili).
