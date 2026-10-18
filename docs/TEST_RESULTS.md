# Risultati test

## 2026-10-18 — Error propagation helper Yocto

- Test helper: `python -m unittest tests.test_yocto_validation_script -v` — PASS, 9 test.
- Fake BitBake restituisce 37; helper propaga exit 37 dopo `bitbake -p`.
- Suite completa `python -m unittest discover -s tests -v` — PASS, 52 test; compileall, `bash -n` su tutti gli script, `git diff --check` — PASS.
- BitBake reale non presente.
