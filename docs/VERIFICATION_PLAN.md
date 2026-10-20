# READY Linux verification plan

Purpose: turn open `STATUS.md` claims into reproducible evidence; never infer real-system success from mocks. Updated 2026-10-20 after the first real BitBake parse and image-graph dry run on a pinned Poky checkout. The user later authorized provisioning, so a non-privileged local checkout and one extracted `lz4` package were used; no system package was installed and no `sudo` was used.

## Current evidence boundary

- Automated suite verifies Python behavior, static Yocto metadata/contracts, QEMU argument safety via fake executables and local artifact-check logic. This is not evidence of actual metadata parsing, image construction, guest boot/SSH, model inference, sandboxing, or performance.
- Read-only `bash scripts/check-yocto-host.sh` on WSL Debian 13/trixie now requires 24 host commands. On the plain system PATH it reports `MISSING lz4c` and exits 1 (`INCOMPLETE`) — correct, because BitBake's `HOSTTOOLS` needs `lz4c` and Debian 13 ships only `lz4`. With the local shim `~/yocto/hosttools` on `PATH` it reports 24/24 `OK`, `bitbake`/`bitbake-layers` `FOUND`, `BUILDDIR` set and `verdict=ready`; a real evidence record was written by `scripts/record-yocto-preflight.py`.
- Gate A (metadata parse) is now verified on this host: Poky `scarthgap` pinned at commit `104772c5fd0653290cbb5e4b77813343957939cc` in `~/yocto/poky-src`, `BUILDDIR=~/yocto/build`, `DISTRO = "readylinux"`, layer registered. `bash scripts/validate-yocto-env.sh` reports `Parsing of 923 .bb files complete ... 0 errors` (single warning: Debian 13 not validated by OE). The parse exposed two real defects that are now fixed: the `readylinux` PN/DISTRO override collision (recipe renamed `readylinux-runtime`) and the missing `usrmerge` distro feature required by the systemd recipe.
- Recipe and graph checks are verified without building: `bitbake -e readylinux-runtime` and `bitbake -e readylinux-console` resolve their `RDEPENDS`/`FILES`/systemd variables, and `bitbake -n readylinux-image` completes 5006 noexec tasks. QEMU tools alone still do not suffice: no READY image or kernel artifact exists, so Gate B (build) and Gate C (boot) remain unverified.
- Record each actual build attempt using `YOCTO_BUILD_EVIDENCE_TEMPLATE.md` and schema. Retain logs and checksums; never mark a gate passed without evidence.

## Gated work packages

| Gate | Scope and prerequisites | Commands / test | Acceptance evidence | Status |
|---|---|---|---|---|
| A — Layer metadata parse | Maintainer-provisioned Linux host, release-pinned Poky/OE-Core, compatible layer set, `BUILDDIR` | `bash scripts/check-yocto-host.sh`; source selected release env; `bash scripts/validate-yocto-env.sh` (`bitbake -p`) | Exact commits, layer series, MACHINE, BitBake version and successful parse log in unique evidence record | Blocked here: BitBake/OE absent, BUILDDIR unset. Requires an already provisioned host (or explicit future provisioning authorization) |
| B — Image build + artifact | Gate A passes; enough disk/RAM; normal OE sources available locally or downloads explicitly authorized | `bitbake readylinux-image`; `sha256sum <artifact>` | Exit 0; retained log; artifact path/format/size/digest; provenance | Not run: no parsed metadata, image build can fetch source |
| C — VM boot + base smoke | Gate B artifact and matching kernel verified; Linux QEMU host | `scripts/verify-image-artifact.sh`; `scripts/boot-image-qemu.sh <image> <sha256> <machine>` with SSH disabled | Serial log; READY prompt; unprivileged service identity; persistent state; BASIC/offline smoke; getty mask evidence | Not run: no image/kernel artifact; QEMU helpers tested only with fake tools |
| D — Guest SSH test access | Gate C boots; image includes/enables SSH daemon and approved user/key policy; no credentials committed | Opt in with `READY_QEMU_SSH_PORT=<port>`; helper maps host `127.0.0.1:<port>` to guest `:22`; connect `ssh -p <port> <user>@127.0.0.1` | Real handshake and selected command outputs retained; host mapping stays loopback-only; no host-network exposure | Helper argument gate tested with fakes only; guest service and SSH handshake not verified |
| E — Model catalog/import | Model/license/provenance selected and provisioning explicitly authorized; otherwise local fixtures only | Schema/catalog unit tests; fake HTTP + temp paths for corrupt digest, interruption, activation/removal | Catalog pins revision/quantization/license/size/hash/runtime/RAM/context; failures preserve verified model; offline import documented | Not implemented/verified; no download authorized or performed |
| F — CPU inference | Gate E model plus CPU-built llama.cpp on consenting Linux host and sufficient RAM/storage | Verify artifact digest; capture runtime revision/build flags; fixed prompt/context, warmups/repeats | Actual response; tokens/s, time-to-first-token, peak RSS, CPU/temp, cancellation/output validity | Not run: no real model/runtime evidence; mock AI tests do not count |
| G — Safe generated-code execution | Threat model and user-approved actual isolation facility | Adversarial FS/network/process/resource escape tests and approval/rollback checks | Isolation boundaries evidenced; subprocess/static lint alone never counts as sandbox | Not implemented/verified |
| H — GPU/ARM64/performance | Selected target hardware/emulator, matching BSP/driver, Gates A-C first | Reproducible target build/boot and workload matrix; CPU fallback | Exact target/kernel/driver/build provenance; repeated workload logs, P95/P99 | Deferred until target hardware and build evidence available |

## Independent local work while blocked

1. Improve unit/static tests for metadata, recipe sources, shell gates, QEMU argument construction, artifact verification, offline model-import logic.
2. Keep IT/EN `STATUS`, `TEST_RESULTS`, roadmap and this plan synchronized with actual command outputs, skip counts and blockers.
3. Never call mock output a real build/boot/inference. Provisioning is allowed only when the task explicitly authorizes it, must stay unprivileged where possible, and must be recorded with exact pins and commands.

## Exit rule

A gate is verified only by its listed acceptance evidence. Missing prerequisites block that gate, not unrelated local work. Resume a blocked gate only once prerequisites are actually present or the user explicitly authorizes provisioning.
