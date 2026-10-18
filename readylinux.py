#!/usr/bin/env python3
"""ReadyLinux: terminal-based, code-first environment for GNU/Linux.

MVP inspired by the immediate programming experience of home computers.
It uses Python, not Commodore BASIC, and does not replace the Linux kernel.
"""

from __future__ import annotations

import argparse
import code
import os
import re
import sys
import traceback
from pathlib import Path

from ai_local import AIConfig, AIError, LocalAI, default_config
from basic import BasicError, BasicProgram
from vibe import VibeWorkspace, VibeError, VIBE_HELP

PROGRAM_LINE = re.compile(r"^(\d{1,7})(?:\s(.*))?$")
PROGRAM_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

HELP_TEXT = """Commands:
  10 print('Ciao')     Store/replace a numbered Python line
  10                   Delete numbered line 10
  LIST                 Show numbered program
  RUN                  Run numbered program
  NEW                  Clear program and reset variables
  SAVE nome            Save program as nome.rdy
  LOAD nome            Load program from nome.rdy
  EXPORT nome          Export executable Python source as nome.py
  BASIC                Enter separate READY BASIC mode
  FILES                List saved .rdy programs
  RESET                Reset Python variables without clearing program
  AI HELP              Show AI commands
  AI STATUS            Check local CPU AI status
  AI START             Start local llama-server (requires GGUF model)
  AI STOP              Stop only the server started by READY
  AI ASK domanda       Ask local AI (also sees numbered program)
  AI EXPLAIN           Explain numbered program
  AI REVIEW            Review code for errors and improvements
  AI FIX               Suggest fixes; never applies them
  CLS                  Clear terminal
  HELP                 Show commands
  QUIT                 Exit

Without a line number, type Python for immediate execution:
  print(2 + 2)
  x = 7
A multiline Python statement ends with an empty line.
For blocks in saved programs, preserve indentation after line numbers.
"""


class ReadyLinux:
    def __init__(self, workspace: Path, ai_config: AIConfig | None = None):
        self.workspace = workspace.expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.program: dict[int, str] = {}
        self.basic = BasicProgram()
        self.basic_mode = False
        self.python_block_expected = False
        self.legacy_mode = False
        self.ai = LocalAI(ai_config or default_config(), self.workspace.parent / "logs")
        self.vibe = VibeWorkspace(self.workspace / "projects", self.ai)
        self.reset_console()

    def reset_console(self) -> None:
        self.namespace = {"__name__": "__main__"}
        self.console = code.InteractiveConsole(locals=self.namespace, filename="<READY immediate>")
        self.continuation = False

    def _file(self, name: str, suffix: str) -> Path:
        if not PROGRAM_NAME.fullmatch(name):
            raise ValueError("Nome non valido: usa lettere, numeri, _ o -; niente percorsi.")
        return self.workspace / (name + suffix)

    def source(self) -> str:
        return "\n".join(self.program[line] for line in sorted(self.program)) + "\n"

    def listing(self) -> str:
        return "\n".join(f"{line} {self.program[line]}" for line in sorted(self.program))

    def save(self, name: str) -> Path:
        path = self._file(name, ".rdy")
        lines = self.listing()
        path.write_text(lines + ("\n" if lines else ""), encoding="utf-8")
        return path

    def load(self, name: str) -> Path:
        path = self._file(name, ".rdy")
        replacement: dict[int, str] = {}
        for index, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = PROGRAM_LINE.fullmatch(raw)
            if match is None or match.group(2) is None:
                raise ValueError(f"Formato .rdy non valido, riga {index}.")
            replacement[int(match.group(1))] = match.group(2)
        self.program = replacement
        self.continuation = False
        return path

    def export(self, name: str) -> Path:
        path = self._file(name, ".py")
        path.write_text(self.source(), encoding="utf-8")
        return path

    def run(self) -> None:
        if not self.program:
            print("Nessun programma: inserisci una riga numerata.")
            return
        try:
            executable = compile(self.source(), "<READY program>", "exec")
            exec(executable, self.namespace)
        except (Exception, KeyboardInterrupt):
            traceback.print_exc()

    def ai_command(self, arg: str) -> None:
        operation, _, question = arg.partition(" ")
        operation = operation.upper()
        question = question.strip()
        if operation == "HELP" and not question:
            print("AI STATUS | AI START | AI STOP | AI ASK domanda | AI EXPLAIN | AI REVIEW | AI FIX")
            print("CPU-only: GGUF + llama.cpp necessari. Nessuna modifica automatica ai file.")
        elif operation == "STATUS" and not question:
            print(self.ai.status())
        elif operation == "START" and not question:
            print(self.ai.start())
        elif operation == "STOP" and not question:
            print(self.ai.stop())
        elif operation in {"ASK", "EXPLAIN", "REVIEW", "FIX"} and (operation == "ASK" or not question):
            print("\n[IA LOCALE - RISPOSTA NON VERIFICATA]\n" + self.ai.ask(operation, self.source(), question) + "\n")
        else:
            print("ERRORE: comando IA non riconosciuto. Usa AI HELP.")

    def basic_command(self, raw: str) -> bool:
        """Handle one command in explicit BASIC mode."""
        text = raw.strip()
        if not text:
            return True
        numbered = re.fullmatch(r"(\d{1,6})(?:\s+(.*))?", text)
        if numbered:
            try:
                self.basic.edit(text)
            except BasicError as exc:
                print(f"BASIC ERROR: {exc}")
            return True
        command, _, arg = text.partition(" ")
        command, arg = command.upper(), arg.strip()
        try:
            if command in {"STOP", "QUIT", "EXIT"} and not arg:
                self.basic_mode = False
                print("READY.")
            elif command == "HELP" and not arg:
                print("BASIC: numbered lines, LIST, RUN, NEW, SAVE name, LOAD name, EDIT n, STOP")
            elif command == "LIST" and not arg:
                print(self.basic.listing() or "(empty BASIC program)")
            elif command == "RUN" and not arg:
                self.basic.run()
            elif command == "NEW" and not arg:
                self.basic.lines.clear()
                self.basic.variables.clear()
                print("BASIC program cleared.")
            elif command == "EDIT" and arg.isdigit():
                line = int(arg)
                print(f"{line} {self.basic.lines[line]}" if line in self.basic.lines else "line not found")
            elif command in {"SAVE", "LOAD"}:
                if not PROGRAM_NAME.fullmatch(arg):
                    raise BasicError(f"{command} requires a valid program name")
                path = self._file(arg, ".bas")
                if command == "SAVE":
                    path.write_text(self.basic.listing() + ("\n" if self.basic.lines else ""), encoding="utf-8")
                    print(f"Saved: {path}")
                else:
                    replacement = BasicProgram(step_limit=self.basic.step_limit)
                    replacement.load_source(path.read_text(encoding="utf-8"))
                    self.basic = replacement
                    print(f"Loaded: {path}")
            else:
                raise BasicError(f"unknown BASIC command: {text}")
        except (OSError, BasicError, ValueError) as exc:
            print(f"BASIC ERROR: {exc}")
        return True

    def command(self, raw: str) -> bool:
        """Process a line. Return False to quit."""
        if self.continuation:
            self.continuation = self.console.push(raw)
            return True
        if self.basic_mode:
            return self.basic_command(raw)
        match = PROGRAM_LINE.fullmatch(raw)
        if self.python_block_expected and match and match.group(2) and match.group(2)[:1].isspace():
            self.program[int(match.group(1))] = match.group(2)
            return True
        if self.python_block_expected and match and match.group(2) and match.group(2).strip().lower().startswith(("for ", "while ", "if ", "elif ", "else:", "try:", "except", "with ", "def ", "class ")):
            match = None
        elif self.python_block_expected and match and match.group(2):
            self.python_block_expected = False
        basic_keywords = ("PRINT", "LET", "INPUT", "IF", "GOTO", "GOSUB", "FOR", "NEXT", "REM", "END", "STOP", "RETURN")
        is_basic_source = bool(match and match.group(2) and re.match(r"^(?:" + "|".join(basic_keywords) + r")(?:\s|$)", match.group(2).strip(), re.I))
        if match and is_basic_source and not self.program and not self.legacy_mode:
            self.basic_mode = True
            try:
                self.basic.edit(raw)
            except BasicError as exc:
                print(f"BASIC ERROR: {exc}")
            return True
        is_python_block = bool(match and match.group(2) and re.match(r"^(?:for|while|if|elif|else|try|except|with|def|class)\b", match.group(2).strip(), re.I))
        if match and is_python_block:
            if self.program:
                self.program[int(match.group(1))] = match.group(2)
                self.python_block_expected = True
                return True
        if match and not is_basic_source:
            number = int(match.group(1))
            source = match.group(2)
            if source is None or source == "":
                self.program.pop(number, None)
            else:
                self.program[number] = source
                self.python_block_expected = source.rstrip().endswith(":")
            return True
        stripped = raw.strip()
        if not stripped:
            return True
        command, _, arg = stripped.partition(" ")
        command = command.upper()
        arg = arg.strip()
        try:
            if command in {"QUIT", "EXIT"} and not arg:
                return False
            if command == "LEGACY" and not arg:
                self.legacy_mode = True
                print("READY Python mode. BASIC enters BASIC mode.")
                return True
            if command == "BASIC" and not arg:
                self.legacy_mode = True
                self.basic_mode = True
                print("READY BASIC. Type HELP for commands; STOP returns to READY.")
                return True
            if command == "HELP" and not arg:
                print(VIBE_HELP)
            elif command in {"BASIC", "LEGACY"} and arg.upper() == "HELP":
                print(HELP_TEXT)
            elif command == "PROGETTI" and not arg:
                print(self.vibe.projects())
            elif command == "PROGETTO":
                kind, _, name = arg.partition(" ")
                kind, name = kind.upper(), name.strip()
                if kind == "NUOVO" and name:
                    print(self.vibe.select(name, create=True))
                elif kind == "USA" and name:
                    print(self.vibe.select(name))
                else:
                    print("Usa PROGETTO NUOVO nome oppure PROGETTO USA nome.")
            elif command == "FILE" and arg.upper() == "PROGETTO":
                print(self.vibe.files())
            elif command in {"CREA", "MODIFICA", "CORREGGI"} and arg:
                print(self.vibe.propose(arg))
            elif command in {"DIFFERENZE", "DIFF"} and not arg:
                print(self.vibe.diff())
            elif command == "APPLICA" and not arg:
                print(self.vibe.apply())
            elif command == "ANNULLA" and not arg:
                print(self.vibe.cancel())
            elif command == "INDIETRO" and not arg:
                print(self.vibe.undo())
            elif command == "VERIFICA" and not arg:
                print(self.vibe.check())
            elif command == "ESEGUI":
                parts = arg.split()
                if len(parts) != 2:
                    print("Per eseguire codice NON isolato: ESEGUI nome.py CONFERMO")
                else:
                    print(self.vibe.run_explicit(*parts))
            elif command == "PY" and arg:
                self.continuation = self.console.push(arg)
            elif command == "LIST" and not arg:
                print(self.listing() or "(programma vuoto)")
            elif command == "RUN" and not arg:
                self.run()
            elif command == "NEW" and not arg:
                self.program.clear()
                self.reset_console()
                print("Memoria programma pulita.")
            elif command == "RESET" and not arg:
                self.reset_console()
                print("Variabili azzerate.")
            elif command == "SAVE" and arg:
                print(f"Salvato: {self.save(arg)}")
            elif command == "LOAD" and arg:
                print(f"Caricato: {self.load(arg)}")
            elif command == "EXPORT" and arg:
                print(f"Esportato: {self.export(arg)}")
            elif command == "FILES" and not arg:
                names = sorted(path.stem for path in self.workspace.glob("*.rdy") if path.is_file())
                print("\n".join(names) if names else "(nessun programma salvato)")
            elif command == "AI":
                self.ai_command(arg)
            elif command == "CLS" and not arg:
                print("\033[2J\033[H", end="")
            else:
                # Natural-language first, preserving explicit/recognizable Python syntax.
                python_prefixes = ("print(", "import ", "from ", "def ", "class ", "for ",
                                   "while ", "if ", "try:", "with ", "return ", "raise ",
                                   "async ", "await ", "#", "@")
                looks_like_python = (raw.lstrip().startswith(python_prefixes) or
                                     "=" in raw or raw.rstrip().endswith(":"))
                if " " in stripped and not looks_like_python:
                    print(self.vibe.propose(stripped))
                else:
                    # Legacy immediate Python mode: UNSANDBOXED, use only trusted code.
                    self.continuation = self.console.push(raw)
        except (OSError, ValueError, AIError, VibeError) as exc:
            print(f"ERRORE: {exc}")
        return True

    def interact(self) -> None:
        print("\nREADY LINUX 0.3 | VIBE-FIRST + LOCAL CPU AI")
        print(f"Progetti: {self.vibe.root} | Attivo: {self.vibe.project}")
        print("Descrivi cosa vuoi creare in italiano, oppure HELP | AI START | QUIT")
        print("READY.\n")
        try:
            while True:
                try:
                    raw = input("... " if self.continuation else "> ")
                except EOFError:
                    print()
                    break
                except KeyboardInterrupt:
                    print("\nInterrotto. Digita QUIT per uscire.")
                    self.reset_console()
                    continue
                if not self.command(raw):
                    break
        finally:
            self.ai.stop()


def main() -> int:
    parser = argparse.ArgumentParser(description="Code-first Linux programming environment")
    parser.add_argument(
        "--workspace", type=Path,
        default=Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))) / "readylinux" / "programs",
        help="Directory dei programmi salvati",
    )
    parser.add_argument("--run", metavar="NAME", help="Esegui un programma salvato e termina")
    parser.add_argument("--ai-model", type=Path, help="Percorso del modello GGUF locale")
    parser.add_argument("--ai-server", help="Percorso del binario llama-server")
    parser.add_argument("--ai-port", type=int, default=18080, help="Porta HTTP locale (default 18080)")
    parser.add_argument("--ai-threads", type=int, help="Numero di thread CPU per IA")
    args = parser.parse_args()
    try:
        ai_config = default_config(model=args.ai_model, server=args.ai_server,
                                   port=args.ai_port, threads=args.ai_threads)
    except ValueError as exc:
        parser.error(str(exc))
    app = ReadyLinux(args.workspace, ai_config=ai_config)
    if args.run:
        try:
            app.load(args.run)
        except (OSError, ValueError, AIError) as exc:
            print(f"ERRORE: {exc}", file=sys.stderr)
            return 1
        app.run()
        return 0
    app.interact()
    return 0


if __name__ == "__main__":
    sys.exit(main())
