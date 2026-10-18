import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai_local import AIConfig, AIError, LocalAI
from vibe import VibeWorkspace


class SimulatedServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/health':
            self.send_error(404)
            return
        raw = b'{"status":"ok"}'
        self.send_response(200)
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path != '/v1/chat/completions':
            self.send_error(404)
            return
        self.server.last_payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        reply = json.dumps({'summary': 'Simulazione', 'files': [{'path': 'main.py', 'content': 'print(42)\n'}]})
        raw = json.dumps({'choices': [{'message': {'content': reply}, 'finish_reason': 'stop'}]}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.httpd = ThreadingHTTPServer(('127.0.0.1', 0), SimulatedServer)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        cfg = AIConfig(model=self.root/'m.gguf', server='unused', port=self.httpd.server_port, timeout=2)
        self.ai = LocalAI(cfg, self.root/'logs')
        self.v = VibeWorkspace(self.root/'projects', self.ai)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(2)
        self.temp.cleanup()

    def test_generate_json_http_then_apply_check_and_undo(self):
        response = self.v.propose('Crea un mini programma')
        self.assertIn('NON APPLICATA', response)
        self.assertEqual(self.httpd.last_payload['response_format'], {'type': 'json_object'})
        self.assertEqual(self.httpd.last_payload['stream'], False)
        self.assertTrue(self.httpd.last_payload['max_tokens'] >= 1400)
        self.assertIn('Crea un mini programma', self.httpd.last_payload['messages'][1]['content'])
        file = self.v.root/'progetto/main.py'
        self.assertFalse(file.exists())
        self.v.apply()
        self.assertEqual(file.read_text(), 'print(42)\n')
        self.assertIn('0 errori', self.v.check())
        self.v.undo()
        self.assertFalse(file.exists())

if __name__ == '__main__':
    unittest.main()
