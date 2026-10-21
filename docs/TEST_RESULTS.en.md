## 2026-10-20 — LocalAI cleanup when llama-server exits during startup

- `LocalAI.start()` closes the log in `finally`, including when the child exits immediately and raises `AIError`; new test intercepts `Popen`/`sleep`, simulates exit code 9, verifies the retained log, `_log_file=None`, and exit code shown by `status()`.
- New test verifies idempotence when an already owned process is alive: no binary resolution, second `Popen`, or log.
- Final suite for this firing: 233 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Local AI startup when the port is occupied

- Two `LocalAI.start()` tests: refuses an occupied loopback port without calling `subprocess.Popen` or creating `llama-server.log`; if READY already owns the running server process, it does not launch a duplicate.
- Test uses an OS-assigned ephemeral IPv4 `127.0.0.1` socket; no external network or real model.
- Suite: 233 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

# Test Results

## 2026-10-20 — BASIC coverage for REM/END/STOP, booleans and false IF; `NOT` bug

- Six new tests in `tests/test_basic.py`: ignored `REM` lines, `END` and `STOP` halting execution, `AND`/`OR`/`NOT` and `<>` operators, a false `IF` that does not jump, string comparison with assignment, and bare `PRINT` emitting an empty line.
- **Real bug found**: `PRINT NOT 0` failed with "invalid expression:  not  0" because the `NOT` substitution added leading spaces and `ast.parse(..., mode="eval")` rejects indentation. Fix: `source.strip()` before parsing.
- **Newly documented behaviour**: boolean results print `True`/`False`, not 1/0 — added to `docs/BASIC.md` and `docs/BASIC.en.md`.
- Suite: 231 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — BASIC documentation ↔ implementation parity

- New `tests/test_basic_docs.py` module (5 tests): compares the keywords claimed by both IT/EN documents, checks that every language keyword exists in `basic.py`, that the console commands (`LIST`, `RUN`, `NEW`, `HELP`, `STOP`, `SAVE`, `LOAD`, `EDIT`) exist in `readylinux.py`, and that both documents keep the "not full Commodore compatibility" disclaimer and the "this restriction is not a sandbox" warning.
- Bugs found in the tests themselves during the firing: `RUN` is a console command, not a language keyword → extraction limited to the "## Language implemented" line; the Italian sandbox regex contained an accented character that did not match → replaced with `non.{0,20}una sandbox`.
- Suite: 233 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Roadmap M1 aligned with the real console and BASIC

- `docs/ROADMAP.en.md` M1 still claimed: "standalone `basic.py` plus 9 focused tests; console integration, persistence commands, bilingual user docs, and full green suite remain incomplete". All four statements were false: `readylinux.py` integrates `BasicProgram` with `SAVE`/`LOAD`, `docs/BASIC.md` and `docs/BASIC.en.md` exist, BASIC tests are 11 and the suite is green.
- The EN text was rewritten to match the IT one: reduced implementation with tests, console integration with persistence, bilingual docs, green suite, full Commodore compatibility not claimed.
- New `test_roadmap_m1_claims_match_console_and_basic_reality`: requires `BasicProgram`/`SAVE`/`LOAD` in the console, both BASIC docs, and forbids "remain incomplete" or a missing caveat.
- Suite: 220 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — OE series recorded in build evidence

- `docs/YOCTO_BUILD_EVIDENCE.schema.json` now requires `identity.oe_series`, matching the validator gate that reads `LAYERSERIES_COMPAT_core`: a build record can no longer omit the OE series it was produced against.
- Example updated with the `"oe_series": "UNVERIFIED"` placeholder; IT/EN templates carry the "OE release series (from `LAYERSERIES_COMPAT_core`, e.g. scarthgap)" line.
- New `test_build_evidence_records_the_oe_release_series` checks the required field, the example placeholder and the line in both templates.
- Suite: 219 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Offline validation of stored evidence records

- `scripts/record-yocto-preflight.py --check PATH` validates an already written record against the recorder's own rules: exact keys (none missing or extra), `schema_version=1`, UTC-shaped `recorded_utc`, 40-hex commit, a `scope` stating "not build evidence", `preflight_exit_code=0`, the `preflight` structure (os/arch/cpus/required/optional/builddir/verdict) and `ready` implying a set builddir and empty `missing_required`. Exit 0 valid, 8 invalid (also broken JSON or a missing file).
- The documented `docs/YOCTO_PREFLIGHT_RECORD.example.json` validates; five new tests cover the valid example, `ready` without builddir, missing/extra keys, a misleading scope, broken JSON and a missing file.
- Suite: 218 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Roadmap and layer README aligned with the verified parse

- `meta-readylinux/README.md` and `README.en.md` claimed **no** series was verified: they now state scarthgap is verified on pinned Poky `104772c5fd06…` with `bitbake -p` at 0 errors, leaving styhead/walnascar/wrynose explicitly unverified.
- `docs/ROADMAP.md` / `ROADMAP.en.md` M2 said "parse not verified" and carried the stale `19/19` tally: updated with the verified parse, 24 host commands, the `lz4c` shim, `bitbake -n` 5006 tasks and the current remaining list (`.wic` build, boot, guest SSH, getty mask, MACHINE).
- Tests updated: the verification-claim regex accepts both "has" and "have"; new `test_roadmap_states_parse_verified_and_build_unverified` forbids `19/19` from returning and requires the pinned commit and the `.wic` mention.
- Suite: 213 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Measurable systemd exposure and threshold gate

- `scripts/validate-systemd-unit.sh` accepts `--security`: it runs `systemd-analyze security --offline=yes` on the temporary copy with the substituted `ExecStart`, extracts the score and exits **7** when it exceeds `READY_MAX_EXPOSURE` (default `8.0`). Unknown arguments → exit 64.
- Real WSL Debian 13 run (systemd 257): `Exposure level: 6.7 (limit 8.0)`, exit 0 — the MEDIUM/6.7 value is no longer just historical prose, it is reproducible with one command.
- Tests: systemd module grew from 4 to 8 cases — `systemd-analyze` stubs for 9.5 (exit 7) and 4.2 (exit 0), a real `--security` run, and an unknown argument (exit 64).
- Suite: 212 tests PASS (26 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Artifact contract enforced by the validator

- `scripts/validate-yocto-env.sh`, after `bitbake -p`, queries `bitbake-getvar --recipe readylinux-image --value IMAGE_FSTYPES`; when `wic` is missing it exits **6** instead of declaring the environment valid. A missing `bitbake-getvar` prints a non-fatal NOTE.
- Real WSL/Poky scarthgap run: `Image fstypes:  tar.bz2 ext4 wic`, exit 0.
- Tests: `bitbake-getvar` stub in the helper; two new cases (`tar.bz2 ext4` → exit 6; `ext4 wic` → exit 0 with the printed value). Validator module: 19 tests.
- Suite: 208 tests PASS (23 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — `.wic` artifact aligned with the documentation

- Docs and the `verify-image-artifact.sh` / `boot-image-qemu.sh` helpers consume a `.wic`, but the image recipe set no `IMAGE_FSTYPES`: `core-image-minimal` defaults to `tar.bz2 ext4`, so the documented file would never be produced.
- Fix: `IMAGE_FSTYPES:append = " wic"` in `readylinux-image.bb`, with a comment explaining why.
- Offline verification via `bitbake -e readylinux-image` (no fetch): `IMAGE_FSTYPES=" tar.bz2 ext4 wic"`, `IMAGE_INSTALL="packagegroup-core-boot  readylinux-runtime readylinux-console"`.
- New `test_image_recipe_produces_the_documented_wic_artifact`: single `IMAGE_FSTYPES` assignment, `wic` present, and IT/EN READMEs mentioning `.wic` and `IMAGE_FSTYPES`.
- Suite: 206 tests PASS (21 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — OE series compatibility verified before parsing

- `scripts/validate-yocto-env.sh` reads `LAYERSERIES_COMPAT_core` from the `core` layer `conf/layer.conf` reported by `bitbake-layers show-layers` and compares it with `LAYERSERIES_COMPAT_readylinux`: no intersection exits 5 without running the parse; an unreadable `core` layer or `layer.conf` exits 4.
- Real WSL/Poky scarthgap run: `Layer collection: readylinux (priority 8)` + `OE series: scarthgap`, then `bitbake -p` without errors.
- Tests: helper extended with a synthetic `core` layer; two new cases (compatible series → prints `OE series: styhead`; unlisted `kirkstone` → exit 5). Validator module: 17 tests.
- Suite: 205 tests PASS (21 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Layer registration gate before parsing

- `scripts/validate-yocto-env.sh` now queries `bitbake-layers show-layers`: the layer path must appear in the report, the collection must be `readylinux`, and the priority must be numeric; otherwise exit 4. A missing `bitbake-layers` exits 2.
- Real WSL run: `Layer collection: readylinux (priority 8)` followed by `bitbake -p` with 0 errors.
- Tests: helper extended with a `bitbake-layers` stub; two new cases (wrong collection → exit 4; report with a different path → exit 4). Module total 15 tests.
- Suite: 203 tests PASS (19 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — User installer tests (`install.sh`, `setup-ai-cpu.sh`)

- New `tests/test_install_script.py` module (5 tests) for the two scripts that were covered only by syntax checks.
- `install.sh`: real run with temporary `HOME`/`XDG_DATA_HOME` — copies `readylinux.py`, `ai_local.py`, `vibe.py` into `$XDG_DATA_HOME/readylinux/app`, creates an executable wrapper in `$HOME/.local/bin` with a bash shebang and the absolute app path, and creates nothing outside the temporary home; fail-closed with missing `python3` (exit 1).
- `setup-ai-cpu.sh`: opt-in CPU-only checks, pinned model SHA-256 `cc324af0…`, `sha256sum -c` verification, no `sudo`/`systemctl`, and fail-closed (exit 1, no files) when tools are missing.
- Bug found in the tests themselves: with an emptied `PATH`, invoking `bash` failed on WSL (fixed by using the absolute path on POSIX and `bash` on Windows).
- Suite: 201 tests PASS (17 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Verification plan realigned with real evidence

- `docs/VERIFICATION_PLAN.md` still claimed "no downloads allowed", "19/19 commands" and "do not claim the layer parses": all superseded by facts. Updated with the pinned Poky `104772c5fd0653290cbb5e4b77813343957939cc`, `BUILDDIR=~/yocto/build`, `0 errors` parse, the `readylinux-runtime` and `usrmerge` fixes, 24 host commands, the `lz4c` shim and `bitbake -n readylinux-image` 5006 noexec tasks.
- New guard `test_verification_plan_records_the_pinned_parse_evidence` prevents the plan from drifting back to "parse not run" or the 19-command tally.
- Suite: 196 tests PASS (17 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — Preflight extended: `lz4c` and real BitBake tools

- scarthgap BitBake requires `lz4c`, absent on Debian 13: the 19-command probe claimed `ready` while BitBake failed with `HOSTTOOLS ... lz4c unavailable`. A real false positive.
- `required_commands` grew from 19 to 24: added `lz4c`, `patch`, `perl`, `tar`, `xargs` (all in `HOSTTOOLS` from `meta/conf/bitbake.conf`).
- On the system PATH: `MISSING lz4c` → `INCOMPLETE` (correct). With `~/yocto/hosttools` on `PATH`: 24/24 `OK`, `bitbake` `FOUND`, `BUILDDIR=~/yocto/build`.
- Real evidence recorded: `python3 scripts/record-yocto-preflight.py …` → `verdict: ready`, `readylinux_commit: 13800fdd…`, `recorded_utc: 2026-10-20T20:36:37Z`, `missing_required: []`, `builddir.set: true`.
- Suite: 195 tests PASS (17 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.

## 2026-10-20 — `usrmerge` distro feature fix and image graph (noexec)

- Recipe verification via `bitbake -e` (no fetch, no build): `readylinux-runtime` resolves `PN=readylinux-runtime`, `PV=0.3`, package-specific `RDEPENDS` and `FILES` covering `/usr/share/readylinux` and `/usr/bin/readylinux`.
- `bitbake -e readylinux-console` **failed**: `ERROR: Nothing RPROVIDES 'systemd' ... systemd was skipped: missing required distro feature 'usrmerge'`. A metadata parse alone did not reveal this.
- Fix: `DISTRO_FEATURES:append = " systemd usrmerge"` in `conf/distro/readylinux.conf`; tests updated to require `usrmerge`.
- After the fix: `bitbake -e readylinux-console` → `RDEPENDS:readylinux-console=" readylinux-runtime systemd"`, `FILES` include unit and mask, `SYSTEMD_SERVICE`/`SYSTEMD_AUTO_ENABLE` correct.
- `bitbake -n readylinux-image` (dry run, no execution and no fetch): `Attempted 5006 tasks ... all succeeded`, including `readylinux-image.bb:do_build`. One warning: Debian 13 not validated by OE.
- Suite: 195 tests PASS (17 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- Still unverified: real image build (needs source fetch), QEMU boot, guest SSH, getty mask in image, artifact hash.

## 2026-10-20 — First real BitBake parse (pinned Poky scarthgap)

- Host: WSL Debian 13, unprivileged user. Commands: `bash scripts/check-yocto-host.sh` (19/19 `OK`, `qemu` found, `bitbake` absent, `BUILDDIR` unset before provisioning).
- Unprivileged local provisioning: `git fetch --depth 1` of Poky commit `104772c5fd0653290cbb5e4b77813343957939cc` (scarthgap) into `~/yocto/poky-src`; missing `lz4c` solved with `apt-get download lz4` + `dpkg -x` into `~/yocto/hosttools` (no `sudo`, no system install).
- `source oe-init-build-env ~/yocto/build` + `bitbake-layers add-layer /mnt/d/repos/ReadyLinux/meta-readylinux` + `DISTRO = "readylinux"` in `local.conf`.
- First `bash scripts/validate-yocto-env.sh`: **failed** with 5 real QA errors in the runtime recipe — `pn-overrides` (PN `readylinux` colliding with the distro) and `pkgvarcheck` on non package-specific `RDEPENDS`/`FILES`.
- Fix: recipe renamed to `readylinux-runtime_0.3.bb`, `IMAGE_INSTALL:append = " readylinux-runtime readylinux-console"`, console `RDEPENDS` on `readylinux-runtime`.
- Second run: `Parsing of 923 .bb files complete (503 cached, 420 parsed). 1881 targets, 49 skipped, 0 masked, 0 errors.` exit 0; single warning: Debian 13 not validated by OE.
- Full suite after the rename: 195 tests PASS (17 Windows skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- Still unverified: image build, QEMU boot, guest SSH, getty mask in image, artifact hash.

## 2026-10-20 — Preflight evidence correction and 174-test baseline

- `bash scripts/check-yocto-host.sh` run from the Windows shell (Git Bash) is not a Debian host: it reports `/etc/os-release` unavailable and missing tools. That output is not Yocto evidence and must not be recorded.
- Correct command, run inside WSL Debian 13: `wsl -d Debian -- /bin/bash -c 'cd /mnt/d/repos/ReadyLinux && /bin/bash scripts/check-yocto-host.sh'`; exit 1 `INCOMPLETE`, 19/19 required host commands `OK`, `qemu-system-x86_64` and `sha256sum` found, `bitbake`/`bitbake-layers` absent, `BUILDDIR` unset.
- Added a test requiring the IT/EN STATUS files to record the WSL Debian result and forbidding Windows-shell output to be stored as host evidence.
- Full suite: 179 tests PASS (10 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13; `compileall`, `bash -n` and `git diff --check` pass.
- No download, install, BitBake parse, image build or QEMU boot performed.
- New `scripts/record-yocto-preflight.py` records the `--json` report with commit/UTC and a "preflight-only, not build evidence" scope; it refuses to write a non-`ready` verdict (exit 3) or to overwrite without `--force` (exit 4). Suite: 184 tests PASS (13 Windows skips).
- Added `docs/YOCTO_PREFLIGHT_RECORD.schema.json` with a placeholder example and tests for record structure and recorder output; a `ready` verdict must agree with builddir and BitBake. Suite: 188 tests PASS (14 Windows skips).
- `scripts/check-yocto-host.sh` now fails closed on the environment: with no readable `/etc/os-release` it exits 2 `NOT-A-LINUX-HOST` (`WRONG-ENVIRONMENT`), because Windows-shell output is not host evidence. Exit 0 = ready, 1 = `INCOMPLETE`, 2 = wrong environment. Suite: 175 tests PASS.

- Stricter recorder: a report claiming `ready` with non-empty `missing_required` or an unset `builddir` is rejected (exit 5) and nothing is written; 2 tests added. Suite: 190 tests PASS (14 Windows skips).

- Script tracking: `install.sh`, `setup-ai-cpu.sh`, `scripts/*.sh` and `scripts/*.py` were committed as `100644` (not executable); restored `100755` via `git update-index --chmod=+x` and added the `test_tracked_scripts_keep_the_executable_bit` guard. Suite: 191 tests PASS (14 Windows skips).

- Layer README parity: new test compares IT/EN command blocks, `scripts/*.sh|py` references, and that every referenced script exists. Suite: 192 tests PASS.

- Pre-parse gate: `scripts/validate-yocto-env.sh` now rejects a `DISTRO` other than `readylinux` (exit 3) and prints a NOTE when `local.conf` sets no DISTRO; 3 dedicated tests. Suite: 195 tests PASS (17 Windows skips).

## 2026-10-18 — Offline Yocto contracts and regression suite

- Runtime recipe regression asserts `inherit allarch`, repository-local `file://` application sources, no model/network payload and declared Python dependencies. Distro test checks systemd is appended without removing inherited features and is selected as init manager.
- Historical WSL systemd-security result: `systemd-analyze security --offline`, MEDIUM/6.7, UMask 0027.
- Static contracts cover layer metadata and explicitly unverified compatibility candidates; local recipe sources, package closure and launcher-to-service `ExecStart`; getty-mask symlink ownership/image inclusion; READY home, persistent StateDirectory and UMask; plus preflight evidence.
- Relevant regressions pass; full suite: 126 tests PASS (8 platform-specific skips) on Windows/Python 3.11 and WSL Debian 13/Python 3.13.
- No BitBake metadata parse, image build or QEMU boot: BitBake/OE checkout and `BUILDDIR` are absent; no install/download performed.

## 2026-10-18 — Firing-start snapshot and host probe

- Initial snapshot verified by `git rev-parse HEAD`: `92abaae72d9023bb82718ff48e0918ebc17f4b23`; `git status --short --branch` = `main...origin/main` with untracked `.pi-loop.json` and `raw` (0 bytes).
- WSL read-only probe `bash scripts/check-yocto-host.sh`: exit 1 `INCOMPLETE`; 19/19 required commands present; BitBake/bitbake-layers absent; `BUILDDIR` unset.
- Commands: `python -m compileall -q readylinux.py ai_local.py vibe.py basic.py`; `python -m unittest discover -s tests -v`; `bash -n install.sh setup-ai-cpu.sh scripts/validate-yocto-env.sh scripts/validate-systemd-unit.sh scripts/verify-image-artifact.sh scripts/check-yocto-host.sh scripts/boot-image-qemu.sh`; `git diff --check`.
- No fetch/install, Yocto parse/build, image build or real QEMU boot.
