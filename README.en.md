# READY Linux 0.3 — Vibe Coding First, Local CPU AI

Licensed under [MIT](LICENSE).

**Describe software in natural language → review proposed files → approve → verify → iterate.**

READY 0.3 is a terminal-based Linux application prototype, not a bootable distribution, graphical desktop, or fully autonomous coding agent. It retains numbered Python programming and optional local AI. An experimental READY BASIC interpreter is available via `BASIC` mode; see [BASIC docs](docs/BASIC.en.md). Existing Python numbered mode remains default.

## Requirements

- GNU/Linux, Python 3.10+, Python standard library.
- Optional local generation: `llama-server` and compatible GGUF model.
- CPU inference supported; no GPU required.
- AI model download is explicit via setup script; real GGUF inference is not verified by current automated tests.

## Quick start

```bash
python3 readylinux.py
```

In READY, type `BASIC`, then:

```text
10 PRINT "HELLO"
20 PRINT 2+2
RUN
STOP
```

Use `HELP` for commands. Python mode is unchanged. See `README.md` for full Italian documentation and caveats. No automatic execution of AI-proposed code.
