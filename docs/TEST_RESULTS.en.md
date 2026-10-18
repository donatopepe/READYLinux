# Test Results

## 2026-10-18 — Test report and Git snapshot consistency

- Initial snapshot verified: `git status --short --branch` showed `main...origin/main`; HEAD `e4f6dacb72d5c0a2548ec7dc4d305531fce2ae05`.
- IT/EN status files align to that snapshot and distinguish later documentation-only commits.
- Standard commands: `python -m unittest discover -s tests -v`; `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `bash -n` for the shell scripts listed below.
- Limitations: no real BitBake/Yocto parse, image build, or QEMU boot.
- Pre-new-test baseline: 78 Windows tests (1 expected skip) and 78 WSL tests; rerun the updated suite.
