# Risultati test

## 2026-10-18 — Consistenza baseline status

- Status IT/EN riallineati a HEAD `c6d98eda388edb1085c74c8812a4484ae26399cf`, test 75, WSL/Windows, limiti BitBake/boot e misura systemd MEDIUM/UMask.
- Nuovo test statico verifica commit citato, limiti host, assenza build claim e UMask in entrambi gli status.
- Windows/Python 3.11 suite — PASS, 76 test; WSL Debian 13/Python 3.13 suite — PASS, 76 test.
- Compileall e shell syntax su entrambi — PASS; `git diff --check` — PASS.
