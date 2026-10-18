# Risultati test

## 2026-10-18 — Immagine senza pesi AI

- Test statici verificano che image recipe non dichiari `SRC_URI`, URL, modello GGUF o runtime llama; runtime recipe ammette solo sorgenti software locali.
- Documentazione precisa che i pesi/runtime AI non sono inclusi e provisioning resta esplicito.
- `python -m unittest discover -s tests -v` — PASS, 52 test; compileall, `bash -n` e `git diff --check` — PASS.
- BitBake assente: contenuto effettivo immagine non verificato.
