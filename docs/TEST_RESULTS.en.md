# Test Results

## 2026-10-18 — Yocto layer and preflight static checks

- Historical WSL systemd security review: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Layer tests cover collection/pattern/priority, unique compatibility-series values, and bilingual README wording that candidate series remain unverified pending a release-pinned parse.
- Full suite: 122 tests PASS, 8 platform-specific skips, on Windows and WSL.

## 2026-10-18 — Firing-start snapshot

- Initial snapshot SHA1 from `git rev-parse HEAD`: `94ec6466d0fa7d01b6b48ffd0405882514251264`.
- `git status --short --branch`: `main...origin/main`, untracked `.pi-loop.json` and `raw` (0 bytes).
- WSL read-only `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required host commands present; BitBake/bitbake-layers/BUILDDIR absent; no package changes.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No Yocto parse/build, image build or real QEMU boot.
