# READY Linux 0.3 — Vibe Coding First, Local CPU AI

Licensed under [MIT](LICENSE).

**Describe software in natural language → review proposed files → approve → verify → iterate.**

READY 0.3 is a terminal-based application prototype, not a bootable Linux distribution, graphical desktop, or autonomous coding agent. It retains the numbered Python workflow and optional local AI. Experimental BASIC mode is entered with `BASIC`; use `HELP` for commands and `STOP` to return to READY. See [BASIC guide](docs/BASIC.en.md) and [Italian README](README.md).

## Requirements

- GNU/Linux, Python 3.10+, standard library.
- Optional generation: local `llama-server` and compatible GGUF model.
- CPU-only supported; no GPU required.
- Model download is opt-in via setup script. Real GGUF inference is not covered by automated tests.

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
