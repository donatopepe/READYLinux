"""Vibe-first local project workflow for READY Linux.

No model output is executed. Edits are previewed, explicitly approved, confined
under a selected project, and can be undone after application. Python execution
is a separate explicit, UNSANDBOXED operation.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ai_local import AIError, LocalAI

PROJECT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,47}\Z")
EXTENSIONS = {".py", ".txt", ".md", ".json", ".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".toml", ".yaml", ".yml"}
MAX_FILES = 5
MAX_CHARS_PER_FILE = 14000
MAX_TOTAL_CHARS = 28000
MAX_CONTEXT_CHARS = 12000
MAX_REQUEST_CHARS = 2000
META = ".ready_history.json"

class VibeError(Exception):
    pass


def _hash(data: str | None) -> str | None:
    return hashlib.sha256(data.encode("utf-8")).hexdigest() if data is not None else None


def _safe_relative(name: str) -> Path:
    if not isinstance(name, str) or len(name) > 160 or "\\" in name or not name:
        raise VibeError("Percorso file non valido.")
    candidate = PurePosixPath(name)
    parts = candidate.parts
    if (candidate.is_absolute() or len(parts) > 5 or
        any(p in (".", "..") or p.startswith(".") or not p for p in parts) or
        any(not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}", p) for p in parts) or
        candidate.suffix.lower() not in EXTENSIONS):
        raise VibeError(f"Percorso non consentito: {name!r}.")
    return Path(*parts)


def _atomic_write(path: Path, content: str) -> None:
    """Write with replacement rather than opening targets (also avoids hardlink writes)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".ready-tmp-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        os.chmod(name, 0o600)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@dataclass
class Proposal:
    project: str
    summary: str
    changes: dict[str, str]
    before: dict[str, str | None]


class VibeWorkspace:
    def __init__(self, root: Path, ai: LocalAI):
        self.root = root.expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.ai = ai
        self.project = "progetto"
        self.pending: Proposal | None = None
        self.last_execution: str = ""

    def _project_dir(self, project: str | None = None, create: bool = False) -> Path:
        name = project or self.project
        if not PROJECT_NAME.fullmatch(name):
            raise VibeError("Nome progetto non valido (lettere, numeri, - o _).")
        directory = self.root / name
        if directory.is_symlink():
            raise VibeError("Progetto simbolico non consentito.")
        if create:
            directory.mkdir(parents=True, exist_ok=True)
        if directory.exists() and not directory.is_dir():
            raise VibeError("Percorso progetto non e' una directory.")
        return directory

    def select(self, name: str, create: bool = False) -> str:
        target = self._project_dir(name, create=create)
        if not target.is_dir():
            raise VibeError("Progetto inesistente. Usa PROGETTO NUOVO nome.")
        self.project = name
        self.pending = None
        self.last_execution = ""
        return f"Progetto attivo: {name} ({target})"

    def projects(self) -> str:
        names = [p.name for p in self.root.iterdir() if p.is_dir() and not p.is_symlink() and PROJECT_NAME.fullmatch(p.name)]
        return "Progetti: " + (", ".join(sorted(names)) or "nessuno")

    def _target(self, name: str, create_parent: bool = False) -> Path:
        relative = _safe_relative(name)
        root = self._project_dir()
        if not root.is_dir():
            raise VibeError("Il progetto non esiste. Usa PROGETTO NUOVO nome.")
        current = root
        for part in relative.parts[:-1]:
            current = current / part
            if current.is_symlink():
                raise VibeError("Link simbolici vietati nel percorso.")
            if current.exists() and not current.is_dir():
                raise VibeError("Un componente del percorso non e' una cartella.")
        path = root / relative
        if path.is_symlink():
            raise VibeError("Non e' consentito modificare link simbolici.")
        if path.exists() and not path.is_file():
            raise VibeError("Il file di destinazione non e' un file regolare.")
        return path

    def _read(self, name: str) -> str | None:
        path = self._target(name)
        if not path.exists():
            return None
        if path.stat().st_size > MAX_CHARS_PER_FILE * 4:
            raise VibeError(f"File troppo grande: {name}.")
        try:
            value = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            raise VibeError(f"File non UTF-8: {name}.") from exc
        if len(value) > MAX_CHARS_PER_FILE:
            raise VibeError(f"File troppo grande: {name}.")
        return value

    def files(self) -> str:
        root = self._project_dir()
        if not root.exists():
            return "Nessun progetto attivo creato. Usa PROGETTO NUOVO nome."
        result = []
        for p in sorted(root.rglob("*")):
            if p.is_symlink():
                continue
            if p.is_file() and not any(part.startswith(".") for part in p.relative_to(root).parts):
                result.append(p.relative_to(root).as_posix())
        return "\n".join(result[:100]) or "(progetto vuoto)"

    def context(self) -> str:
        root = self._project_dir()
        if not root.exists():
            return "(progetto vuoto)"
        parts, consumed = [], 0
        for name in self.files().splitlines():
            try:
                value = self._read(name)
            except VibeError:
                continue
            if value is None or len(value) + consumed > MAX_CONTEXT_CHARS:
                continue
            parts.append(f"=== {name} ===\n{value}")
            consumed += len(value)
            if len(parts) >= 5:
                break
        return "\n".join(parts) or "(nessun file testuale leggibile)"

    def _stage(self, payload: dict) -> str:
        if not isinstance(payload, dict) or not isinstance(payload.get("files"), list):
            raise VibeError("Risposta IA non valida: atteso oggetto JSON con files[].")
        self.pending = None  # Invalid model output must not leave an older proposal active.
        files = payload["files"]
        if not 1 <= len(files) <= MAX_FILES:
            raise VibeError(f"Una proposta deve contenere tra 1 e {MAX_FILES} file.")
        changes, before = {}, {}
        total = 0
        for entry in files:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("content"), str):
                raise VibeError("Ogni file deve avere path e content testuali.")
            name, content = entry["path"], entry["content"]
            _safe_relative(name)
            if name in changes:
                raise VibeError(f"File duplicato nella risposta: {name}.")
            total += len(content)
            if len(content) > MAX_CHARS_PER_FILE or total > MAX_TOTAL_CHARS:
                raise VibeError("Proposta troppo grande: suddividere in modifiche piu' piccole.")
            before[name] = self._read(name)
            changes[name] = content
        summary = payload.get("summary", "Modifica proposta dal modello")
        if not isinstance(summary, str):
            summary = "Modifica proposta dal modello"
        self.pending = Proposal(self.project, summary[:300], changes, before)
        return self.diff()

    def stage_json(self, raw: str) -> str:
        """Parse untrusted model JSON; never execute it."""
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError) as exc:
            raise VibeError("Il modello non ha prodotto JSON valido. Ripeti la richiesta o prova un modello migliore.") from exc
        return self._stage(data)

    def propose(self, request: str) -> str:
        if not request.strip() or len(request) > MAX_REQUEST_CHARS:
            raise VibeError(f"Descrizione richiesta non valida (massimo {MAX_REQUEST_CHARS} caratteri).")
        if not self._project_dir().exists():
            self._project_dir(create=True)
        self.pending = None  # Never retain stale proposals if inference fails.
        reply = self.ai.propose_project(request, self.context(), self.last_execution)
        return self.stage_json(reply)

    def diff(self) -> str:
        if self.pending is None or self.pending.project != self.project:
            return "Nessuna modifica proposta. Descrivi cosa vuoi creare."
        parts = [f"PROPOSTA (NON APPLICATA): {self.pending.summary}"]
        for name, content in self.pending.changes.items():
            old = self.pending.before[name]
            preview = "".join(difflib.unified_diff((old or "").splitlines(True), content.splitlines(True),
                                                   fromfile=f"prima/{name}" if old is not None else "/dev/null",
                                                   tofile=f"dopo/{name}"))
            # Do not interpret model-supplied ANSI/terminal controls while previewing.
            sanitized = "".join(c if c in "\n\t" or ord(c) >= 32 and ord(c) != 127 else repr(c)[1:-1] for c in preview)
            parts.append(sanitized[:10000] if preview else f"{name}: nessuna differenza")
        parts.append("Scrivi APPLICA per salvare oppure ANNULLA per scartare. Il codice NON verra' eseguito.")
        return "\n".join(parts)

    def _metadata(self) -> Path:
        target = self._project_dir() / META
        if target.is_symlink():
            raise VibeError("Metadati di ripristino non sicuri.")
        return target

    def apply(self) -> str:
        p = self.pending
        if p is None or p.project != self.project:
            raise VibeError("Nessuna proposta da applicare.")
        # Refuse to overwrite changes made since proposal was shown.
        for name, original in p.before.items():
            if self._read(name) != original:
                raise VibeError(f"Il file {name} e' cambiato: rigenera la proposta.")
        history_path = self._metadata()
        prior_history = history_path.read_text(encoding="utf-8") if history_path.exists() else None
        written = []
        try:
            for name, content in p.changes.items():
                path = self._target(name)
                _atomic_write(path, content)
                written.append(name)
            record = {"time": int(time.time()), "before": p.before,
                      "after_hash": {key: _hash(value) for key, value in p.changes.items()}}
            _atomic_write(history_path, json.dumps(record, ensure_ascii=False, indent=2))
        except Exception as exc:
            for name in reversed(written):
                path = self._target(name)
                before = p.before[name]
                if before is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, before)
            if prior_history is None:
                history_path.unlink(missing_ok=True)
            else:
                _atomic_write(history_path, prior_history)
            raise VibeError(f"Applicazione fallita, ripristino tentato: {exc}") from exc
        self.pending = None
        self.last_execution = ""
        return f"Modifica applicata a {len(written)} file. Usa INDIETRO per ripristinare l'ultima modifica."

    def cancel(self) -> str:
        self.pending = None
        return "Proposta annullata. Nessun file modificato."

    def undo(self) -> str:
        path = self._metadata()
        if not path.exists():
            raise VibeError("Nessuna modifica precedente da ripristinare.")
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            before, after = record["before"], record["after_hash"]
            if not isinstance(before, dict) or not isinstance(after, dict) or set(before) != set(after):
                raise ValueError("invalid history")
        except (ValueError, KeyError, TypeError) as exc:
            raise VibeError("Storico di ripristino non valido.") from exc
        # Prevent overwriting user's subsequent edits; validate ALL before changing ANY.
        for name, original in before.items():
            if original is not None and not isinstance(original, str):
                raise VibeError("Storico di ripristino non valido.")
        for name, digest in after.items():
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise VibeError("Storico di ripristino non valido.")
            if _hash(self._read(name)) != digest:
                raise VibeError(f"File {name} modificato dopo APPLICA: non ripristino automaticamente.")
        for name, original in before.items():
            if original is None:
                self._target(name).unlink(missing_ok=True)
            elif isinstance(original, str):
                _atomic_write(self._target(name), original)
            else:
                raise VibeError("Storico di ripristino non valido.")
        path.unlink()
        self.pending = None
        return "Ultima modifica ripristinata."

    def check(self) -> str:
        root = self._project_dir()
        if not root.is_dir():
            raise VibeError("Progetto inesistente.")
        checked, errors = 0, []
        for path in sorted(root.rglob("*.py")):
            if path.is_symlink() or any(p.startswith(".") for p in path.relative_to(root).parts):
                continue
            rel = path.relative_to(root).as_posix()
            try:
                text = self._read(rel)
                ast.parse(text or "", filename=rel)
                checked += 1
            except (SyntaxError, VibeError) as exc:
                errors.append(f"{rel}: {exc}")
        for path in sorted(root.rglob("*.json")):
            if path.is_symlink() or any(p.startswith(".") for p in path.relative_to(root).parts):
                continue
            rel = path.relative_to(root).as_posix()
            try:
                json.loads(self._read(rel) or "")
                checked += 1
            except (json.JSONDecodeError, VibeError) as exc:
                errors.append(f"{rel}: {exc}")
        status = f"Analisi statica: {checked} file Python/JSON validi; {len(errors)} errori. NESSUN codice eseguito."
        return status + ("\n" + "\n".join(errors[:20]) if errors else "")

    def run_explicit(self, filename: str, confirm: str) -> str:
        if confirm != "CONFERMO":
            raise VibeError("Esecuzione NON isolata: usa ESEGUI nome.py CONFERMO solo per codice fidato.")
        if not filename.endswith(".py"):
            raise VibeError("In questa versione si possono eseguire solo file .py.")
        file = self._target(filename)
        if not file.is_file():
            raise VibeError(f"File non trovato: {filename}.")
        result = None
        try:
            # Not a sandbox. stdout/stderr captured; resource/network restrictions unavailable.
            result = subprocess.run([sys.executable, "-E", "-s", str(file)], cwd=self._project_dir(),
                                    capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL,
                                    errors="replace")
            output = (result.stdout + "\n" + result.stderr)[:8000]
            self.last_execution = f"File: {filename}; returncode: {result.returncode}\n{output}"[-8000:]
            return f"Processo terminato: codice {result.returncode}.\n{output}"
        except subprocess.TimeoutExpired:
            self.last_execution = f"File: {filename}; timeout 10 secondi"
            return "Processo interrotto dopo 10 secondi (timeout)."


VIBE_HELP = """READY VIBE — scrivi direttamente cosa vuoi creare, oppure usa:
  PROGETTO NUOVO nome      Crea e seleziona un progetto
  PROGETTO USA nome        Seleziona un progetto esistente
  PROGETTI                Elenca progetti
  FILE PROGETTO           Visualizza file del progetto
  CREA descrizione        Genera una proposta con IA locale
  MODIFICA descrizione    Propone modifiche ai file esistenti
  CORREGGI descrizione    Propone modifiche, anche dall'ultimo errore di esecuzione
  DIFFERENZE              Mostra il diff proposto
  APPLICA                 Salva solo modifiche approvate
  ANNULLA                 Scarta la proposta
  INDIETRO                Ripristina l'ultima modifica applicata
  VERIFICA                Controlla sintassi Python/JSON SENZA eseguire codice
  ESEGUI nome.py CONFERMO  Esegue codice fidato (NON sandboxato)
  AI START / AI STATUS     Avvia e controlla llama.cpp CPU
  AI STOP                 Arresta solo il server avviato da READY
  PY istruzione           Esegui Python manualmente (vecchia modalita')
  HELP                    Mostra comandi e informazioni
  QUIT                    Esci

Se manca il modello, puoi creare e sfogliare progetti, eseguire VERIFICA e usare INDIETRO.
Generare e modificare richiede il server GGUF pronto. Nessuna modifica avviene prima di APPLICA.
"""
