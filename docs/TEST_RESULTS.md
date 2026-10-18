# Risultati test

## 2026-10-18 — Avviso segreti template evidenze

- Template IT/EN esplicitano di redigere segreti/non allegare credenziali nei checksum config.
- Test mirato `python -m unittest tests.test_yocto_scaffold.YoctoScaffoldTests.test_build_evidence_templates_include_required_provenance_and_results -v` — PASS.
- Suite completa `python -m unittest discover -s tests -v` — PASS, 57 test; compileall, `bash -n`, `git diff --check` — PASS.
- Nessun dato reale o build inseriti.
