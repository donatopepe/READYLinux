# Verifiable Roadmap

## M0 — Baseline (documented)

Acceptance: repository structure, verified capabilities/limitations, reproducible test commands recorded.

## M1 — Classic console and BASIC

Acceptance: real parser/runtime; numbered lines, variables, expressions, conditions, loops, I/O, subroutines and files; deterministic tests; no regression to READY/Python legacy. Current state: standalone `basic.py` plus 9 focused tests; console integration, persistence commands, bilingual user docs, and full green suite remain incomplete.

## M2 — Minimal OS build

Scaffold started: `meta-readylinux` layer metadata, distro config, image recipe, local runtime recipe, systemd tty1 service, and static tests. BitBake parse/build and x86-64 QEMU boot remain unverified. Observed WSL Debian 13 preflight: 19/19 required host commands OK, QEMU found, but BitBake/bitbake-layers absent and BUILDDIR unset (see [verification plan](VERIFICATION_PLAN.md)). Next acceptance: pin supported Yocto release and machine; validate `bitbake -p`, build image and boot on a provisioned OE host. No kernel tuning without benchmarks.

## M3 — READY Stable

Compatible kernel/BSP and stable profile; verify boot, storage, input, services, and recovery.

## M4 — Performance and low latency

One variable per experiment; identical builds and reproducible benchmarks; record P95/P99 and regressions. External patches require provenance, license, and compatibility evidence.

## M5 — Real CPU inference

Explicitly imported llama.cpp/model; offline CPU inference; measure RAM, latency, and cancellation. Selectable model catalog/purchasing guidance requires provenance, version/license/checksum, offline import and negative-path tests; see [`AI_HARDWARE.en.md`](AI_HARDWARE.en.md) and [Italian](AI_HARDWARE.it.md). Current shopping guidance is an estimate, not live research or a verified benchmark. User-requested hardware web research remains pending; it was not started because no web tool is available and repository rules prohibit initiating network operations.

## M6 — Secure coding agent

Multi-file changes, diff/approval, real isolated tests, CPU/RAM/filesystem/network limits, rollback, negative tests.

## M7 — Workbench/AI Studio

UI process separate from engine; test responsiveness during inference; choose technology based on measurements.

## M8 — GPU and ARM64

Only verified backends/targets; CPU fallback; QEMU ARM64 or specific BSP tested.

## M9 — Release

Images, SBOM/license manifest, installation/recovery, complete test matrix.

## Verification gap gates

Open gaps depend on explicit prerequisites (OE/BitBake host, image/kernel, guest SSH, model, isolation). Use the [gated verification plan](VERIFICATION_PLAN.md) for prerequisites, commands, acceptance evidence and no-download scope; fake-tool tests never close a runtime gate.
