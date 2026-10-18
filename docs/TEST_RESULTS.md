# Risultati test

## 2026-10-18 — Guard template evidenze

- Test mirati: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 9 test.
- Template IT/EN controllati per placeholders provenance, checksum, verdict non verificato e assenza hash commit simili a dati reali.
- Suite completa `python -m unittest discover -s tests -v` — PASS, 55 test; compileall, `bash -n`, `git diff --check` — PASS.
- Build/boot non eseguiti (BitBake/QEMU assenti).
