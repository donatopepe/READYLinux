# READY BASIC (English)

READY BASIC is an explicit optional mode; existing numbered Python mode remains unchanged. Enter with `BASIC`; return to READY with `STOP` (or `QUIT`/`EXIT` inside BASIC).

## Commands

- `10 PRINT "HELLO"` — enter/replace numbered source line.
- `10` — delete line 10.
- `LIST`, `RUN`, `NEW`, `HELP`, `STOP`.
- `SAVE name`, `LOAD name` — workspace-local `.bas` files; names accept letters, digits, `_`, `-`.
- `EDIT n` — show numbered line.

## Language implemented

Boolean results print as `True`/`False`, not as 1/0.

`LET`/assignment, `PRINT`, `INPUT`, arithmetic, comparisons, boolean `AND`/`OR`/`NOT`, `IF condition THEN line`, `GOTO`, `GOSUB`/`RETURN`, `FOR`/`NEXT` with optional `STEP`, `REM`, `END`, `STOP`.

Expressions use an allowlisted AST evaluator; Python calls/attributes and unsupported syntax are rejected. Execution has a configurable statement-step limit. This is a safety restriction, **not** a sandbox for other generated code.

Example:

```basic
10 FOR I=1 TO 3
20 PRINT I
30 NEXT I
40 END
```

Verified interpreter tests cover arithmetic, branches, loops, input, subroutines, persistence, malformed input, rejected calls, and step limits. This BASIC dialect is a small implementation, not full Commodore BASIC compatibility.
