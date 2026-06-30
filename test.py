import threading
import os
import webview
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler


def start_server():
    os.chdir("frontend/dist")

    server = HTTPServer(
        ("127.0.0.1", 8000),
        SimpleHTTPRequestHandler
    )

    server.serve_forever()


threading.Thread(
    target=start_server,
    daemon=True
).start()

class Api:

    def say_hello(self, name):
        print('heeloo')
        return f"Hello {name}"


api = Api()

window = webview.create_window(
    "My App",
    "http://127.0.0.1:8000",
    width=1400,
    height=900,
    js_api=api
)

# webview.start()
webview.start(debug=True)