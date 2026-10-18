# Risultati test

## 2026-10-18 — Baseline corrente, validazione cross-platform

- Windows/MSYS, Python 3.11: `python -m unittest discover -s tests -v` — PASS, 66 test.
- WSL2 Debian 13, Python 3.13: `python3 -m unittest discover -s tests -v` — PASS, 66 test.
- In entrambi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` e `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh` — PASS.
- `systemd-analyze verify` su copia temporanea unit, ExecStart sostituito — PASS; non prova image integration/runtime.
- `systemd-analyze security --offline`: score exposure 6.7, MEDIUM; UMask 0027 residuo documentato.
- `git diff --check` — PASS.
- BitBake non disponibile; nessun Yocto parse/build/QEMU boot o image hash reale.
