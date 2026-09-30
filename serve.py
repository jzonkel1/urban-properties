import os, sys, time, threading, subprocess, http.server, socket, socketserver
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
PORT = 8080
WATCH = ["src/home.html", "build.py"]

def build():
    r = subprocess.run([sys.executable, "build.py"], capture_output=True, text=True)
    print(time.strftime("%H:%M:%S"), (r.stdout or r.stderr).strip(), flush=True)

def mt():
    return tuple(os.path.getmtime(p) if os.path.exists(p) else 0 for p in WATCH)

def watcher():
    last = mt()
    while True:
        time.sleep(0.7)
        cur = mt()
        if cur != last:
            last = cur; time.sleep(0.2); build()

class Quiet(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

class V4(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True; daemon_threads = True
    def handle_error(self, request, client_address):
        pass  # browsers drop keep-alive sockets; not worth a traceback
class V6(V4):
    address_family = socket.AF_INET6

build()
threading.Thread(target=watcher, daemon=True).start()
srv4 = V4(("127.0.0.1", PORT), Quiet)
threading.Thread(target=srv4.serve_forever, daemon=True).start()
try:
    srv6 = V6(("::1", PORT), Quiet)
    threading.Thread(target=srv6.serve_forever, daemon=True).start()
except OSError as e:
    print("ipv6 skipped:", e, flush=True)
print(f"serving http://localhost:{PORT}/  (watching {', '.join(WATCH)})", flush=True)
while True: time.sleep(3600)
