# Risultati test

## 2026-10-18 — Baseline firing hardware guidance

- Snapshot iniziale: `git status --short --branch` mostrava `main...origin/main` e `.pi-loop.json`/`raw` (0 byte) non tracciati; HEAD `5ef5181285cb64446d660452c89538f8aa82e462`.
- Historical WSL systemd assessment: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Status IT/EN updated; guard statico controlla HEAD, count test, limiti BitBake/QEMU.
- Windows/Python 3.11: 109 test PASS (6 skip platform-specific); WSL Debian 13/Python 3.13: 109 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- Guidance hardware mantenuta bilingue e marcata come stima; web research non eseguita per assenza browser tool e vincolo no-network. No inference/model download/Yocto build/QEMU boot.
