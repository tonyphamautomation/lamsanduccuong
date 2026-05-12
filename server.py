import http.server, socketserver, urllib.parse, os

PORT = 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.send_response(302)
            self.send_header('Location', '/duc-cuong-wood.html')
            self.end_headers()
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass  # suppress logs

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server chạy tại: http://localhost:{PORT}")
    httpd.serve_forever()
