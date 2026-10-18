# Risultati test

## 2026-10-18 — Coerenza status/report e evidenze correnti

- Status IT/EN citano esplicitamente lo snapshot HEAD all'inizio di questo firing: `8a287643b5498a307ee8b41e70c85277fcb1b1b0`; non pretendono di indicare l'HEAD dei commit di aggiornamento.
- Test statico verifica in entrambi: commit snapshot, limiti BitBake/QEMU, exposure MEDIUM/UMask.
- `python -m unittest discover -s tests -v` è il comando standard per la suite completa; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py` e `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh` sono i check statici standard.
- Report registra i limiti: BitBake/Yocto parse/build e boot QEMU reali non eseguiti.
- Windows/Python 3.11: 78 test PASS (1 skip previsto: systemd-analyze assente); WSL Debian 13/Python 3.13: 78 test PASS.
- Compileall, shell syntax su entrambi e `git diff --check` — PASS.
- BitBake/Yocto parse, image build e QEMU boot reali non eseguiti.
