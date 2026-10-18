# Verifiable Roadmap

## M0 — Baseline (documented)

Acceptance: repository structure, verified capabilities/limitations, reproducible test commands recorded.

## M1 — Classic console and BASIC

Acceptance: real parser/runtime; numbered lines, variables, expressions, conditions, loops, I/O, subroutines and files; deterministic tests; no regression to READY/Python legacy. Current state: standalone `basic.py` plus 9 focused tests; console integration, persistence commands, bilingual user docs, and full green suite remain incomplete.

## M2 — Minimal OS build

Scaffold started: `meta-readylinux` layer metadata, distro config, image recipe, local runtime recipe, and static tests. BitBake parse/build and x86-64 QEMU boot remain unverified. Next acceptance: pin supported Yocto release and machine; validate `bitbake -p`, build image and boot in QEMU on suitable Linux host. No kernel tuning without benchmarks.

## M3 — READY Stable

Compatible kernel/BSP and stable profile; verify boot, storage, input, services, and recovery.

## M4 — Performance and low latency

One variable per experiment; identical builds and reproducible benchmarks; record P95/P99 and regressions. External patches require provenance, license, and compatibility evidence.

## M5 — Real CPU inference

Explicitly imported llama.cpp/model; offline CPU inference; measure RAM, latency, and cancellation.

## M6 — Secure coding agent

Multi-file changes, diff/approval, real isolated tests, CPU/RAM/filesystem/network limits, rollback, negative tests.

## M7 — Workbench/AI Studio

UI process separate from engine; test responsiveness during inference; choose technology based on measurements.

## M8 — GPU and ARM64

Only verified backends/targets; CPU fallback; QEMU ARM64 or specific BSP tested.

## M9 — Release

Images, SBOM/license manifest, installation/recovery, complete test matrix.
