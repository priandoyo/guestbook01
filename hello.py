
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
import json

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api":
            data = {"server": "hello.py", "port": 8001}
            content = json.dumps(data)
            ctype = "application/json"
        else:
            try:
                with urlopen("http://127.0.0.1:8002/api", timeout=3) as r:
                    data = json.loads(r.read())
                message = json.dumps(data, indent=2)
            except Exception as e:
                message = str(e)

            content = f"""
            <html><body>
            <h1>This is hello.py — Port 8001</h1>
            <h2>Message read from hello2.py — Port 8002</h2>
            <pre>{message}</pre>
            <p><a href="/api">View JSON API</a></p>
            </body></html>
            """
            ctype = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(content.encode())

HTTPServer(("0.0.0.0", 8001), App).serve_forever()
