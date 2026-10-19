# Test Results

## 2026-10-18 — Hardware guidance documentation baseline

- Initial snapshot: `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes); HEAD `5b405a49bbb493a8235ddc33622a48a2465381f3`.
- Previous WSL systemd hardening finding: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static test checks HEAD, test count and BitBake/QEMU limitations in both IT/EN status documents.
- Windows/Python 3.11: 109 tests PASS (6 platform-specific skips); WSL Debian 13/Python 3.13: 109 tests PASS.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n` scripts; `git diff --check`.
- README, roadmap and architecture link the bilingual AI hardware guide and state evidence limits. No web search/download performed.
- No real Yocto parse/build or QEMU boot.
