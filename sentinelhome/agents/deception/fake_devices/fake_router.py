from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

LOG_FILE = "sentinelhome/data/honeypot_hits.log"


class FakeRouterHandler(BaseHTTPRequestHandler):
    def log_attempt(self, username="unknown"):
        with open(LOG_FILE, "a") as f:
            f.write(
                f"[{datetime.datetime.now()}] "
                f"Router admin access attempt from {self.client_address}, "
                f"user={username}\n"
            )

    def do_GET(self):
        if self.path in ["/", "/admin", "/login"]:
            self.log_attempt()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Router Login</title></head>
                <body>
                    <h2>Router Admin Login</h2>
                    <form method="POST">
                        Username: <input name="username"/><br>
                        Password: <input type="password" name="password"/><br>
                        <input type="submit" value="Login"/>
                    </form>
                </body>
                </html>
            """)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()

        username = "unknown"
        if "username=" in data:
            username = data.split("username=")[1].split("&")[0]

        self.log_attempt(username=username)

        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Access Denied")


def start_fake_router(port=8080):
    server = HTTPServer(("0.0.0.0", port), FakeRouterHandler)
    print(f"[HONEYPOT] Fake router admin panel running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    start_fake_router()
