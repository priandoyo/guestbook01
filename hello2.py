
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "server": "hello2.py",
            "port": 8002,
            "message": "Hello from Server 2!"
        }

        if self.path == "/api":
            content = json.dumps(data)
            ctype = "application/json"
        else:
            content = f"""
            <html><body>
            <h1>This is hello2.py — Port 8002</h1>
            <p>Message: {data["message"]}</p>
            <p><a href="/api">View JSON API</a></p>
            </body></html>
            """
            ctype = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(content.encode())

HTTPServer(("0.0.0.0", 8002), App).serve_forever()
