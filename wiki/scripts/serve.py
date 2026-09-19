"""Serve only one public artifact at its production prefix on loopback."""
import argparse,http.server
from pathlib import Path
from urllib.parse import urlsplit
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--port',type=int,default=8766);ap.add_argument('--prefix',default='/Codex-Thronewake/next/');a=ap.parse_args()
root=a.root.resolve()
if not (root/'release.json').is_file():raise ValueError('Serve only a checked release artifact')
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def do_GET(self):
  path=urlsplit(self.path).path
  if not path.startswith(a.prefix):self.send_error(404);return
  self.path='/'+self.path[len(a.prefix):];super().do_GET()
http.server.ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
