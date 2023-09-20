import http.server
import socketserver
import psutil
import time
import json

def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {
        "CPU Usage (%)": cpu_percent,
        "RAM Usage (%)": memory_info.percent
    }

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/info":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            info = get_system_info()
            self.wfile.write(json.dumps(info).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")

def update_info(interval):
    while True:
        with open("info.json", "w") as f:
            info = get_system_info()
            f.write(json.dumps(info))
        time.sleep(interval)

if __name__ == "__main__":
    PORT = 8080
    INTERVAL = 2  # Update interval in seconds

    # Start the info updater in a separate thread
    import threading
    updater_thread = threading.Thread(target=update_info, args=(INTERVAL,))
    updater_thread.daemon = True
    updater_thread.start()

    # Start the HTTP server
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
