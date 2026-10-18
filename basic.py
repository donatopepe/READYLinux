"""Small, safe BASIC interpreter for READY Linux.

Supported statements: LET, assignment, PRINT, INPUT, IF ... THEN line,
GOTO, GOSUB/RETURN, FOR/NEXT, REM, END and STOP. Expressions are parsed with
Python's AST but only an explicit arithmetic/boolean subset is evaluated.
"""
from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass
from typing import Callable


class BasicError(ValueError):
    """Invalid BASIC source or runtime error."""


@dataclass(frozen=True)
class Statement:
    line: int
    source: str


_BINOPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
}
_CMPOPS = {
    ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
    ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
}


def _expression(source: str, variables: dict[str, object]) -> object:
    # BASIC operators; translate only outside quoted strings.
    source = source.replace("<>", "!=")
    source = re.sub(r"(?<![<>=!])=(?!=)", "==", source)
    source = re.sub(r"\bAND\b", " and ", source, flags=re.I)
    source = re.sub(r"\bOR\b", " or ", source, flags=re.I)
    source = re.sub(r"\bNOT\b", " not ", source, flags=re.I)
    try:
        node = ast.parse(source, mode="eval").body
    except SyntaxError as exc:
        raise BasicError(f"invalid expression: {source}") from exc

    def visit(n: ast.AST) -> object:
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float, str, bool)):
            return n.value
        if isinstance(n, ast.Name):
            key = n.id.upper()
            if key not in variables:
                raise BasicError(f"undefined variable: {key}")
            return variables[key]
        if isinstance(n, ast.BinOp) and type(n.op) in _BINOPS:
            try:
                return _BINOPS[type(n.op)](visit(n.left), visit(n.right))
            except (ArithmeticError, TypeError, ValueError) as exc:
                raise BasicError(f"invalid arithmetic: {exc}") from exc
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub, ast.Not)):
            value = visit(n.operand)
            return (not value) if isinstance(n.op, ast.Not) else (+value if isinstance(n.op, ast.UAdd) else -value)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, (ast.And, ast.Or)):
            values = [visit(value) for value in n.values]
            return all(values) if isinstance(n.op, ast.And) else any(values)
        if isinstance(n, ast.Compare):
            left = visit(n.left)
            for op, right_node in zip(n.ops, n.comparators):
                if type(op) not in _CMPOPS:
                    raise BasicError("unsupported comparison")
                right = visit(right_node)
                if not _CMPOPS[type(op)](left, right):
                    return False
                left = right
            return True
        raise BasicError(f"unsupported expression element: {type(n).__name__}")

    return visit(node)


class BasicProgram:
    def __init__(self, *, step_limit: int = 100_000):
        self.lines: dict[int, str] = {}
        self.variables: dict[str, object] = {}
        self.step_limit = step_limit

    def edit(self, text: str) -> None:
        match = re.fullmatch(r"\s*(\d{1,6})(?:\s+(.*))?\s*", text)
        if not match:
            raise BasicError("enter a numbered BASIC line")
        number = int(match.group(1))
        body = (match.group(2) or "").strip()
        if not body:
            self.lines.pop(number, None)
        else:
            self.lines[number] = body

    def load_source(self, source: str) -> None:
        parsed: dict[int, str] = {}
        for raw in source.splitlines():
            if not raw.strip():
                continue
            match = re.fullmatch(r"\s*(\d{1,6})\s+(.+?)\s*", raw)
            if not match:
                raise BasicError(f"invalid program line: {raw}")
            number, body = int(match.group(1)), match.group(2)
            if number in parsed:
                raise BasicError(f"duplicate line: {number}")
            parsed[number] = body
        self.lines = parsed

    def listing(self) -> str:
        return "\n".join(f"{n} {self.lines[n]}" for n in sorted(self.lines))

    def run(self, *, output: Callable[[str], None] | None = None,
            input_fn: Callable[[str], str] | None = None) -> dict[str, object]:
        output = output or print
        input_fn = input_fn or input
        numbers = sorted(self.lines)
        index = {line: i for i, line in enumerate(numbers)}
        pc = 0
        gosub: list[int] = []
        loops: list[tuple[str, object, object, int]] = []
        variables: dict[str, object] = {}
        self.variables = variables
        steps = 0
        while 0 <= pc < len(numbers):
            steps += 1
            if steps > self.step_limit:
                raise BasicError("execution step limit exceeded")
            line_no = numbers[pc]
            text = self.lines[line_no].strip()
            upper = text.upper()
            pc += 1
            if not text or upper.startswith("REM ") or upper == "REM":
                continue
            if upper in ("END", "STOP"):
                break
            if upper == "PRINT":
                output("")
                continue
            if upper.startswith("PRINT "):
                value = _expression(text[6:].strip(), variables)
                output(str(value))
            elif upper.startswith("INPUT "):
                name = text[6:].strip().upper()
                self._check_name(name)
                raw = input_fn(f"{name}? ")
                try:
                    value: object = float(raw) if "." in raw else int(raw)
                except ValueError:
                    value = raw
                variables[name] = value
            elif upper.startswith("GOTO "):
                pc = self._target(text[5:].strip(), index)
            elif upper.startswith("GOSUB "):
                gosub.append(pc)
                pc = self._target(text[6:].strip(), index)
            elif upper == "RETURN":
                if not gosub:
                    raise BasicError(f"RETURN without GOSUB at line {line_no}")
                pc = gosub.pop()
            elif upper.startswith("IF "):
                match = re.fullmatch(r"IF\s+(.+?)\s+THEN\s+(\d{1,6})", text, re.I)
                if not match:
                    raise BasicError(f"invalid IF at line {line_no}")
                if _expression(match.group(1), variables):
                    pc = self._target(match.group(2), index)
            elif upper.startswith("FOR "):
                match = re.fullmatch(r"FOR\s+([A-Za-z][A-Za-z0-9]*)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?", text, re.I)
                if not match:
                    raise BasicError(f"invalid FOR at line {line_no}")
                name = match.group(1).upper()
                self._check_name(name)
                start, end = _expression(match.group(2), variables), _expression(match.group(3), variables)
                step = _expression(match.group(4), variables) if match.group(4) else 1
                if not isinstance(step, (int, float)) or step == 0:
                    raise BasicError("FOR step must be nonzero number")
                variables[name] = start
                loops.append((name, end, step, pc))
            elif upper.startswith("NEXT"):
                if not loops:
                    raise BasicError(f"NEXT without FOR at line {line_no}")
                name, end, step, body_pc = loops[-1]
                if text[4:].strip() and text[4:].strip().upper() != name:
                    raise BasicError(f"NEXT variable mismatch at line {line_no}")
                variables[name] += step
                if (step > 0 and variables[name] <= end) or (step < 0 and variables[name] >= end):
                    pc = body_pc
                else:
                    loops.pop()
            elif upper.startswith("LET "):
                self._assign(text[4:], variables, line_no)
            elif re.match(r"^[A-Za-z][A-Za-z0-9]*\s*=", text):
                self._assign(text, variables, line_no)
            else:
                raise BasicError(f"unknown statement at line {line_no}: {text}")
        return dict(variables)

    @staticmethod
    def _check_name(name: str) -> None:
        if not re.fullmatch(r"[A-Z][A-Z0-9]*", name):
            raise BasicError(f"invalid variable name: {name}")

    @classmethod
    def _assign(cls, text: str, variables: dict[str, object], line: int) -> None:
        match = re.fullmatch(r"\s*([A-Za-z][A-Za-z0-9]*)\s*=\s*(.+)\s*", text)
        if not match:
            raise BasicError(f"invalid assignment at line {line}")
        name = match.group(1).upper()
        cls._check_name(name)
        variables[name] = _expression(match.group(2), variables)

    @staticmethod
    def _target(value: str, index: dict[int, int]) -> int:
        try:
            line = int(value)
            return index[line]
        except (ValueError, KeyError) as exc:
            raise BasicError(f"target line does not exist: {value}") from exc
