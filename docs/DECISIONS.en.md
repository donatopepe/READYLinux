# Decision Log

## D001 — Preserve READY 0.3

Keep ZIP baseline behavior intact; add incrementally without replacing working application.

## D002 — Separate BASIC from Python runtime

The target requires real BASIC, while READY 0.3 uses numbered Python. Keep a distinct interpreter to avoid ambiguous semantics and regressions.

## D003 — Do not claim a sandbox

Static checking and explicit execution do not provide isolation. Never auto-run AI output.

## D004 — No kernel tuning without measurements

Do not add CachyOS patches or performance profiles until kernel/target and reproducible baseline benchmarks exist.

## D005 — Explicit BASIC mode

Enter BASIC with `BASIC`; keep numbered Python in the default READY mode. This avoids language ambiguity and legacy regressions.
