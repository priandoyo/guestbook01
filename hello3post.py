
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
import json

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api":
            data = {"server": "hello3post.py", "port": 8003}
            content = json.dumps(data)
            ctype = "application/json"
        else:
            message = {
                "from": "hello3post.py",
                "port": 8003,
                "message": "Hello from Server 3!"
            }
            try:
                req = Request(
                    "http://127.0.0.1:8004/api",
                    data=json.dumps(message).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urlopen(req, timeout=3) as r:
                    result = json.loads(r.read())
                response = json.dumps(result, indent=2)
            except Exception as e:
                response = str(e)

            content = f"""
            <html><body>
            <h1>This is hello3post.py — Port 8003</h1>
            <h2>JSON message sent to port 8004</h2>
            <pre>{json.dumps(message, indent=2)}</pre>
            <h2>Response from hello4post.py</h2>
            <pre>{response}</pre>
            <p><a href="/api">View JSON API</a></p>
            </body></html>
            """
            ctype = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(content.encode())

HTTPServer(("0.0.0.0", 8003), App).serve_forever()
