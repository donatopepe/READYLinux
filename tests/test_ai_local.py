import contextlib
import io
import json
import socket
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai_local import AIConfig, AIError, LocalAI
from readylinux import ReadyLinux


class DummyLlama(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/health':
            self.send_error(404)
            return
        payload = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        if self.path != '/v1/chat/completions':
            self.send_error(404)
            return
        body = self.rfile.read(int(self.headers['Content-Length']))
        self.server.last_payload = json.loads(body)
        payload = json.dumps({'choices': [{'message': {'content': 'Spiegazione simulata (TEST)'}}]}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        pass


class LocalAITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.httpd = ThreadingHTTPServer(('127.0.0.1', 0), DummyLlama)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.config = AIConfig(model=self.root / 'model.gguf', server='does-not-matter', port=self.httpd.server_port, timeout=3)
        self.app = ReadyLinux(self.root / 'programs', ai_config=self.config)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(3)
        self.temp.cleanup()

    def test_status_existing_local_server(self):
        self.assertIn('online', self.app.ai.status())
        self.assertIn('esterno', self.app.ai.status())

    def test_ask_http_and_program_context(self):
        self.app.program[10] = 'x = 3'
        self.app.program[20] = 'print(x)'
        reply = self.app.ai.ask('EXPLAIN', self.app.source())
        self.assertEqual(reply, 'Spiegazione simulata (TEST)')
        prompt = self.httpd.last_payload['messages'][1]['content']
        self.assertIn('x = 3', prompt)
        self.assertIn('print(x)', prompt)
        self.assertTrue(self.httpd.last_payload['stream'] is False)
        self.assertEqual(self.httpd.last_payload['max_tokens'], 384)

    def test_ai_command_does_not_change_code(self):
        self.app.command('10 print(42)')
        before = self.app.listing()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.app.command('AI REVIEW')
            self.app.command('AI FIX')
            self.app.command('AI ASK Come funziona il codice?')
        self.assertEqual(self.app.listing(), before)
        self.assertIn('Spiegazione simulata', out.getvalue())

    def test_missing_code_and_long_question(self):
        with self.assertRaises(AIError):
            self.app.ai.ask('FIX', '')
        with self.assertRaises(AIError):
            self.app.ai.ask('ASK', '', 'A' * 2001)

    def test_start_refuses_absent_model(self):
        with self.assertRaises(AIError):
            self.app.ai.start()

    def test_stop_does_not_kill_external_process(self):
        self.assertIn('non arresto', self.app.ai.stop())

    def test_start_refuses_an_occupied_port_before_spawning(self):
        model = self.root / "occupied.gguf"
        model.write_bytes(b"GGUF")
        binary = self.root / "llama-server"
        binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        binary.chmod(0o700)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            ai = LocalAI(AIConfig(model=model, server=str(binary), port=port), self.root / "occupied-logs")
            with patch("ai_local.subprocess.Popen") as popen:
                with self.assertRaisesRegex(AIError, "gia' occupata"):
                    ai.start()
            popen.assert_not_called()
        self.assertFalse((self.root / "occupied-logs/llama-server.log").exists())

    def test_start_accepts_its_owned_live_server_without_spawning_duplicate(self):
        model = self.root / "owned.gguf"
        model.write_bytes(b"GGUF")
        binary = self.root / "llama-server"
        binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        binary.chmod(0o700)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            ai = LocalAI(AIConfig(model=model, server=str(binary), port=port), self.root / "owned-logs")
            fake_process = type("FakeProcess", (), {"returncode": None, "poll": lambda self: None})()
            ai.process = fake_process
            with patch("ai_local.subprocess.Popen") as popen:
                result = ai.start()
            popen.assert_not_called()
        self.assertIn("gia' avviato da READY", result)
        self.assertIs(ai.process, fake_process)

    def test_start_logs_child_exit_without_leaking_log_handle(self):
        model = self.root / "early-exit.gguf"
        model.write_bytes(b"GGUF")
        binary = self.root / "llama-server"
        binary.write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")
        binary.chmod(0o700)
        process = type("ExitedProcess", (), {"returncode": 9, "poll": lambda self: 9})()
        ai = LocalAI(AIConfig(model=model, server=str(binary), port=18082), self.root / "early-exit-logs")
        with patch("ai_local.subprocess.Popen", return_value=process):
            with patch("ai_local.time.sleep"):
                with self.assertRaisesRegex(AIError, "terminato subito.*codice 9"):
                    ai.start()
        self.assertIsNone(ai._log_file)
        self.assertTrue((self.root / "early-exit-logs/llama-server.log").is_file())
        self.assertIn("terminato (codice 9)", ai.status())

    def test_start_returns_idempotently_for_a_live_owned_process(self):
        model = self.root / "already-running.gguf"
        model.write_bytes(b"GGUF")
        cfg = AIConfig(model=model, server="missing-binary-is-not-looked-up", port=18083)
        ai = LocalAI(cfg, self.root / "unused-log")
        process = type("LiveProcess", (), {"returncode": None, "poll": lambda self: None})()
        ai.process = process
        with patch("ai_local.subprocess.Popen") as popen, patch.object(ai, "_server_binary") as resolve:
            message = ai.start()
        popen.assert_not_called()
        resolve.assert_not_called()
        self.assertIs(ai.process, process)
        self.assertIn("gia' avviato da READY", message)

    def test_cpu_only_server_flags(self):
        model = self.root / 'model.gguf'
        model.write_bytes(b'GGUF')
        binary = self.root / 'llama-server'
        binary.write_text('#!/bin/sh\nexit 0\n')
        binary.chmod(0o700)
        cfg = AIConfig(model=model, server=str(binary), port=18081, threads=2)
        ai = LocalAI(cfg, self.root / 'logs')
        class FakeProcess:
            returncode = None
            def poll(self):
                return None
            def terminate(self):
                pass
            def wait(self, timeout):
                return 0
        with patch('ai_local.subprocess.Popen', return_value=FakeProcess()) as popen:
            with patch('ai_local.time.sleep'):
                output = ai.start()
        cmd = popen.call_args.args[0]
        self.assertIn('CPU', output)
        self.assertEqual(cmd[cmd.index('--n-gpu-layers') + 1], '0')
        self.assertEqual(cmd[cmd.index('--device') + 1], 'none')
        self.assertEqual(cmd[cmd.index('--host') + 1], '127.0.0.1')
        self.assertIn('--ctx-size', cmd)
        ai.stop()

if __name__ == '__main__':
    unittest.main()
