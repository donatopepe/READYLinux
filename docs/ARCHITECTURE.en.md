# READY Linux Architecture (Incremental Proposal)

## Current state

Python application: `readylinux.py` handles READY console, numbered Python programs, and explicit BASIC mode; `basic.py` implements BASIC runtime with a restricted AST expression evaluator; `ai_local.py` calls local llama.cpp server; `vibe.py` handles workspaces, proposals, diffs, apply/undo, and static checks. Tests live in `tests/`. No OS layer, kernel, GUI, verified sandbox, or embedded build is present.

## Target

1. **Classic runtime:** READY shell independent of AI plus real BASIC runtime, then primary Linux console.
2. **Project agent:** local-inference abstraction; changes only as reviewable patches; real isolated runner.
3. **System image:** Yocto layer separate from runtime; Stable first, Performance only after benchmarks; separate x86-64 and ARM64 images.
4. **UI:** separate UI and inference processes with documented local protocol; Classic remains usable without GUI.

## Security boundaries

The model gets neither unrestricted filesystem access nor privileges. Static checks are not a sandbox. Untrusted generated code stays non-executable automatically until an isolated, tested runner exists. No model/toolchain downloads in the base build.

## Open decisions

Yocto release/BSP, BASIC dialect, GUI toolkit, sandbox runtime, models, and protocols require measured technical spikes; none are assumed.
