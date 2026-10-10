
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class App(BaseHTTPRequestHandler):
    message = {"message": "No message received yet"}

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            App.message = json.loads(self.rfile.read(length))

            result = {"status": "saved", "received": App.message}
            self.send_response(200)
        except Exception:
            result = {"status": "error", "message": "Invalid JSON"}
            self.send_response(400)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_GET(self):
        if self.path == "/api":
            content = json.dumps(App.message)
            ctype = "application/json"
        else:
            content = f"""
            <html><body>
            <h1>This is hello4post.py — Port 8004</h1>
            <h2>Latest JSON message received</h2>
            <pre>{json.dumps(App.message, indent=2)}</pre>
            <p><a href="/api">View JSON API</a></p>
            </body></html>
            """
            ctype = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(content.encode())

HTTPServer(("0.0.0.0", 8004), App).serve_forever()
