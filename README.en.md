# READY Linux 0.3 — Vibe Coding First, Local CPU AI

Licensed under [MIT](LICENSE).

**Describe software in natural language → review proposed files → approve → verify → iterate.**

READY 0.3 is a terminal-based application prototype, not a bootable Linux distribution, graphical desktop, or autonomous coding agent. It retains the numbered Python workflow and optional local AI. Experimental BASIC mode is entered with `BASIC`; use `HELP` for commands and `STOP` to return to READY. See [BASIC guide](docs/BASIC.en.md) and [Italian README](README.md).

## Requirements

- GNU/Linux, Python 3.10+, standard library.
- Optional generation: local `llama-server` and compatible GGUF model.
- CPU-only supported; no GPU required.
- Default model in the optional setup script: **Qwen2.5-Coder-1.5B-Instruct Q4_K_M**, about **1.12 GB GGUF**; total RAM use exceeds file size and grows with context. Speed depends on CPU, RAM, build and prompt; start with a few files.

### Recommended hardware (estimate, not a verified shopping list)

Reviewed 2026-10-18. Conservative capacity guidance for the current model, not measured requirements. The model was not downloaded or benchmarked here; current prices, inventory and SKU recommendations are unverified. No live web research was performed in this pass because no browser/search tool is available and repository rules prohibit initiating network operations.

| Use | Look for | Rationale/limit |
|---|---|---|
| Console without AI | Any distro-supported x86-64, 4 GB RAM | Python/BASIC does not need GGUF; project storage is separate |
| CPU AI, short trials | Recent x86-64 CPU, 4+ cores, 16 GB RAM, SSD with 10+ GB free | Room for OS, model and short context; latency not guaranteed |
| Daily CPU AI | Modern 6–8 cores, 32 GB RAM, 256+ GB NVMe SSD | More room for context and other processes; more cores do not ensure linear scaling |
| Larger models/long contexts later | 64 GB RAM or more; evaluate GPU only after benchmarking the selected model | Outside the tested profile; do not buy a GPU based on this roadmap |

Before purchase, compare current CPU benchmarks, upgradeable dual-channel RAM, storage, noise, power, Linux/driver support and warranty. No brand/model/price/retailer recommendation is made; confirm compatibility and return terms with the seller. Keep this guidance dated and update only after source-backed research and reproducible benchmarks. See [model/hardware selection policy](docs/AI_HARDWARE.en.md) and [Italian](docs/AI_HARDWARE.it.md).

## Quick start

```bash
python3 readylinux.py
```

Optional non-admin installation:

```bash
bash install.sh
~/.local/bin/readylinux
```

To provision local AI (requires Internet and downloads only when explicitly run):

```bash
bash setup-ai-cpu.sh
```

## BASIC example

```text
READY.
> BASIC
READY BASIC.
> 10 PRINT "HELLO"
> 20 PRINT 2+2
> RUN
HELLO
4
> STOP
```

BASIC is an experimental reduced dialect, not full Commodore BASIC compatibility. It evaluates an allowlisted expression subset; this is not a sandbox for arbitrary code. Python mode remains available. See [BASIC docs in English](docs/BASIC.en.md) and [Italian docs](docs/BASIC.md).

## Embedded Linux build scaffold

A minimal Yocto layer is present under `meta-readylinux/`. It installs READY from local sources and does not fetch AI weights. BitBake build has not been run; use a Linux host with a selected Yocto release and machine. See [layer guide (EN)](meta-readylinux/README.en.md) and [Italian guide](meta-readylinux/README.md). This scaffold is not a verified or bootable image.

## Limits and safety

AI proposals are reviewable and not executed automatically. `ESEGUI` and Python `RUN` are ordinary user-permission execution, not sandboxing. This prototype is not a bootable distribution; Yocto, kernel, GUI, real model inference, GPU, ARM64, and secure code-execution isolation remain unimplemented or unverified.
