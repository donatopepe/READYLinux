# Test Results

## 2026-10-18 — Initial snapshot and report consistency

- At firing start, `git status --short --branch` showed `main...origin/main`; snapshot HEAD `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`. This firing's documentation/test commits are subsequent and non-product.
- Static tests ensure IT/EN status cites snapshot, commit, build-host limits and systemd MEDIUM/UMask finding.
- Standard suite/compileall/shell-syntax commands are documented here.
- No real BitBake/Yocto parse, image build, or QEMU boot.
- Windows/Python 3.11: 79 tests PASS (1 expected skip: systemd-analyze unavailable); WSL Debian 13/Python 3.13: 79 tests PASS.
- Compileall, shell syntax on both, and `git diff --check` — PASS.
