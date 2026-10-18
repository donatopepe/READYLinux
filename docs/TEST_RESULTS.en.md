# Test Results

## 2026-10-18 — Ignore local archive files

- Real BitBake/Yocto build and QEMU boot not run; prerequisites remain missing.
- Prior systemd evidence: `systemd-analyze security --offline` on WSL, `MEDIUM/6.7`, UMask 0027.
- Full suite: `python -m unittest discover -s tests -v`.
- Added `.gitignore` rule `*.zip` so local archives are not accidentally included in diff/staging.
- `git check-ignore -v ReadyLinux_0.3_VibeCoding_CPU.zip READYLinux_0.3_Codex_Handoff.zip` — both ignored by `.gitignore:5`.
- Static test covers cache, bytecode, loop lock, GGUF and ZIP patterns.
- Windows/MSYS Python 3.11 suite: 81 tests PASS (1 expected systemd-analyze skip); WSL Debian 13 Python 3.13 suite: 81 tests PASS.
- Verification commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; shell: `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check` — PASS.
