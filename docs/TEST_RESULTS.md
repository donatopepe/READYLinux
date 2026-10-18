# Risultati test

## 2026-10-18 — Ownership stato systemd

- Test statici mirati: `python -m unittest tests.test_yocto_scaffold -v` — PASS, 6 test.
- Verificati `StateDirectory`, mode 0750, `UMask`, XDG path, home/gruppo utente e workspace persistente.
- `python -m unittest discover -s tests -v` — PASS, 52 test; compileall, `bash -n` e `git diff --check` — PASS.
- Nessuna verifica runtime systemd/BitBake disponibile.
