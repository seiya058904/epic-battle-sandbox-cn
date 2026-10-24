"""Loopback-only server for the locally generated build; no directory listings."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import socket
ROOT=Path(__file__).resolve().parents[1]
class Server(ThreadingHTTPServer):
    allow_reuse_address=False
    def server_bind(self):
        if hasattr(socket,'SO_EXCLUSIVEADDRUSE'):self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
        super().server_bind()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        allowed={'/','/index.html','/local.html','/local-mode.js','/prefs-codec.js'}
        allowed.update('/'+str(p.relative_to(ROOT)).replace('\\','/') for folder in ('Build','TemplateData','local-generated') for p in (ROOT/folder).glob('*') if p.is_file())
        if path not in allowed:self.send_error(404);return
        super().do_GET()
    def do_HEAD(self):
        self.send_error(405)
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-EBS-Local','0.1.0')
        super().end_headers()
    def list_directory(self,path):self.send_error(403)
if __name__=='__main__':
    print('http://127.0.0.1:8765/local.html (Ctrl+C to stop)',flush=True)
    Server(('127.0.0.1',8765),Handler).serve_forever()
