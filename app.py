from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from pathlib import Path
from html import escape
from datetime import datetime

# Store messages beside this Python file
FILE = Path(__file__).parent / "messages.txt"


class Guestbook(BaseHTTPRequestHandler):

    def do_GET(self):
        # Read existing messages from the text file
        messages = ""
        if FILE.exists():
            for line in FILE.read_text(encoding="utf-8").splitlines():
                parts = line.split("|", 2)

                # Support both old and new message formats
                if len(parts) == 3:
                    timestamp, name, message = parts
                elif len(parts) == 2:
                    name, message = parts
                    timestamp = "No timestamp"
                else:
                    continue

                messages += (
                    f"<p><small>{escape(timestamp)}</small><br>"
                    f"<b>{escape(name)}</b>: "
                    f"{escape(message)}</p>"
                )

        # HTML is included directly in app.py
        html = f"""
        <html>
        <head><title>Guestbook</title></head>
        <body style="font-family:Arial;max-width:600px;margin:40px auto">
            <h1>My Guestbook</h1>

            <form method="POST">
                <input name="name" placeholder="Your name" required>
                <br><br>
                <textarea name="message" placeholder="Your message"
                    required></textarea>
                <br><br>
                <button type="submit">Submit</button>
            </form>

            <h2>Messages</h2>
            {messages}
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        # Receive name and message from the form
        length = int(self.headers.get("Content-Length", 0))
        if length > 10000:
            self.send_error(413)
            return

        data = self.rfile.read(length).decode("utf-8")
        form = parse_qs(data)

        name = form.get("name", [""])[0].strip()
        message = form.get("message", [""])[0].strip()

        if not name or not message:
            self.send_error(400, "Name and message are required")
            return

        # Keep each message on one line
        name = name.replace("|", "/").replace("\n", " ")
        message = message.replace("|", "/").replace("\n", " ")

        # Add timestamp and save the new message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with FILE.open("a", encoding="utf-8") as f:
            f.write(f"{timestamp}|{name}|{message}\n")

        # Return to the guestbook page
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


print("Guestbook running at http://127.0.0.1:8000")
HTTPServer(("0.0.0.0", 8000), Guestbook).serve_forever()
