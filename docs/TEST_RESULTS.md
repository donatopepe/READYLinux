# Risultati test

## 2026-10-18 — Baseline SSH forwarding QEMU

- Snapshot firing iniziale: `git status --short --branch` = `main...origin/main` con `.pi-loop.json` e `raw` (0 byte) non tracciati; HEAD `4ca49bdd48cbf0ba2f811c2fe1e33d5a951bb855`.
- Historical WSL hardening result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Guard statico status protegge firing HEAD, count suite e limiti BitBake/QEMU IT/EN.
- Windows/Python 3.11: 114 test PASS (8 skip platform-specific); WSL Debian 13/Python 3.13: 114 test PASS.
- Comandi: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` script; `git diff --check`.
- Fake-QEMU tests verificano SSH forwarding solo su loopback, default rete disabilitata, porta invalida rifiutata prima dell'invocazione. No guest SSH/real boot/Yocto build testati.
