# Risultati test

## 2026-10-18 — Protezione archivi locali Git

- BitBake/Yocto build e QEMU boot reali non eseguiti; prerequisiti ancora mancanti.
- Evidenza systemd precedente: `systemd-analyze security --offline` su WSL, `MEDIUM/6.7`, UMask 0027.
- Suite completa: `python -m unittest discover -s tests -v`.
- Aggiunta regola `.gitignore` `*.zip`: archivi locali non entrano per errore nel diff/staging.
- `git check-ignore -v ReadyLinux_0.3_VibeCoding_CPU.zip READYLinux_0.3_Codex_Handoff.zip` — entrambi esclusi da `.gitignore:5`.
- Test statico copre regole cache, bytecode, lock loop, GGUF, ZIP e override sintassi layer/recipes moderni; quest'ultimo non sostituisce bitbake parse.
- Windows/MSYS Python 3.11 suite: 82 test PASS (1 skip previsto: systemd-analyze assente); WSL Debian 13 Python 3.13 suite: 82 test PASS.
- Comandi di verifica: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; shell: `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check` — PASS.
