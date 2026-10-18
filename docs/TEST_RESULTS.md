# Risultati test

## 2026-10-18 — Policy hardening systemd

- `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test.
- Assertion esplicite per User/Group non-root, `NoNewPrivileges`, `ProtectSystem`, `ProtectHome`, `PrivateTmp`, writable state ristretto e assenza capability elevate.
- Suite completa `python -m unittest discover -s tests -v` — PASS, 52 test; compileall, `bash -n` e `git diff --check` — PASS.
- Unit config non validata con systemd/BitBake runtime.
