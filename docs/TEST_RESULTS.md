# Risultati test

## 2026-10-18 — Sequenza comandi build Yocto

- README IT/EN ora mostrano ordine: `oe-init-build-env` → MACHINE in local.conf → add-layer → helper parse-only → build esplicita.
- Test statico controlla ordine e presenza MACHINE.
- `python -m unittest discover -s tests -v` — PASS, 54 test; compileall, `bash -n`, `git diff --check` — PASS.
- BitBake non disponibile.
