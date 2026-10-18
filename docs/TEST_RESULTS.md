# Risultati test

## 2026-10-18 — Snapshot iniziale e consistenza dei report

- All'inizio del firing: `git status --short --branch` mostrava `main...origin/main`; HEAD snapshot `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`. I commit doc di questo firing sono successivi e solo documentali/test.
- Test statici verificano che gli status IT/EN citino lo snapshot, commit, limiti build host e finding systemd MEDIUM/UMask.
- Comandi standard suite/compileall/shell syntax documentati in questo file.
- BitBake/Yocto parse, image build e QEMU boot reali non eseguiti.
- Windows/Python 3.11: 79 test PASS (1 skip atteso: systemd-analyze assente); WSL Debian 13/Python 3.13: 79 test PASS.
- Compileall, shell syntax su entrambi e `git diff --check` — PASS.
