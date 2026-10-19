# READY Linux verification plan

Purpose: turn open claims in `STATUS.md` into reproducible evidence; never infer real-system success from mocks. Status: plan drafted 2026-10-18; no external build/download/SSH/GGUF experiment performed in this pass. This repository's `AGENTS.md` prohibits initiating network, downloads and installs; do not provision missing dependencies without explicit authorization. Can complete unit tests, static checks and documentation independently meanwhile.

## Current evidence boundary

### Observed WSL preflight, 2026-10-18

Command: `bash scripts/check-yocto-host.sh`; result exit 1, `Preflight: INCOMPLETE (read-only; no package changes made)`.

- Debian GNU/Linux 13 (trixie), x86_64, 20 CPUs.
- Required host commands: 19/19 reported `OK` by this probe.
- Found optional tools: `qemu-system-x86_64`, `sha256sum`; absent: `bitbake`, `bitbake-layers`.
- `BUILDDIR` unset: source a maintainer-selected release environment on an already provisioned host before Gate A.
- Do not install/clone BitBake or Poky during this task: repository `AGENTS.md` and current user request prohibit installs/downloads/network. This environment report does not imply metadata parse readiness.

- The automatic suite covers Python behavior, static Yocto metadata/contracts, QEMU argument construction via fake executables, and local artifact checks. It does not prove a Yocto parse, an image build, boot, guest SSH, model inference, sandboxing or performance.
- `command -v bitbake` is absent; no Poky/OE checkout is present. QEMU binaries were observed on Windows, but there is no READY image/kernel artifact verified for boot. Do not run boot helper against arbitrary host files.
- Build evidence must be recorded per attempt using `YOCTO_BUILD_EVIDENCE_TEMPLATE.md` and its schema. Never record a success without retained raw command output/artifact digest.

## Gated work packages

| Gate | Scope and prerequisites | Commands / test | Acceptance evidence | Status |
|---|---|---|---|---|
| A — Layer metadata parse | A maintainer-provisioned Linux host with release-pinned Poky/OE-Core, compatible layer set and `BUILDDIR`; approved provisioning if needed | `bash scripts/check-yocto-host.sh`; source selected release environment; `bash scripts/validate-yocto-env.sh` (`bitbake -p`) | Full commits, layer series, MACHINE, BitBake version and successful parse log in a new evidence record | Blocked: BitBake/OE tree absent; no fetch/install allowed here |
| B — Image build + artifact | Gate A passes; enough disk/RAM; source downloads explicitly authorized or fully cached | `bitbake readylinux-image`; `sha256sum <artifact>` | Exit 0, retained build log, artifact format/size/digest, exact provenance | Not run; builds can fetch source and require a provisioned host |
| C — VM boot + base smoke | Gate B artifact and matching kernel verified; QEMU on Linux host; explicit kernel cmdline | Verify artifact; run `scripts/boot-image-qemu.sh <image> <sha256> <machine>` with no SSH first | Serial log, READY tty, getty mask, unprivileged service user, persistent state and BASIC/offline tests recorded | Not run; no READY image/kernel artifact |
| D — Guest SSH test access | Gate C boots; guest image has an SSH daemon enabled, account/key policy and documented authorized-key provisioning; `READY_QEMU_SSH_PORT` free | Set port; start helper; `ssh -p <port> <user>@127.0.0.1`; run selected smoke tests | Fake test proves loopback-only hostfwd argument and fail-closed invalid ports; real evidence additionally needs guest SSH handshake and command results | Host-side CLI support now exists; guest service/handshake unverified |
| E — Model catalog + offline import | Model choice/license/provenance approved; source accessible via user's authorized provisioning or offline artifact | Unit tests using local fixtures/fake HTTP only; separately verify real downloaded/imported artifact digest | Catalog includes immutable revision, quantization, license, size/hash, runtime/RAM/context, import/removal path; corrupted/interrupted import must not activate or overwrite verified models | Not implemented/verified; don't download |
| F — CPU inference | Gate E model and compatible `llama-server` built for CPU, consented capable Linux host, adequate free disk/RAM | Explicit setup; digest check; capture build revision/options; fixed prompt/context warm-up + repeated benchmark | Retain actual response, time-to-first-token, tokens/s, peak RSS, CPU/temperature, cancellation and output validity; distinguish mock from real inference | Not run; no model/runtime benchmark |
| G — Safe code execution/sandbox | Threat model + user-approved isolation primitive available on test host | Adversarial tests for filesystem/network/process/CPU/RAM escape, approval and rollback | Demonstrated isolation boundaries; plain subprocess/static lint must never count as sandbox | Not implemented/verified |
| H — GPU/ARM64/performance | Selected target hardware/emulator and matching BSP/driver; gates A–C first | Reproducible build + benchmark matrix, CPU fallback; ARM64 QEMU/BSP only if present | Exact target/kernel/driver/build provenance, boot and workload logs, repeated measurements/P95/P99; no hardware-buying claim from unsupported guesses | Deferred until target and measurements exist |

## Immediate no-prerequisite work

1. Keep focused negative-path/static tests and offline docs up to date.
2. Run host-independent full tests, compileall and shell syntax; report platform skips accurately.
3. For every future real attempt, use a unique evidence record; retain command output and artifact hashes outside tracked source when large/sensitive.

## Exit rule

A gate is `verified` only by its acceptance evidence, not by the existence of helper scripts, green fakes, or roadmap prose. Record blockers and continue only independent local work; never convert a blocker into an unsupported claim.
