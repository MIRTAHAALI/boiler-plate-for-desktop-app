import os
import threading
import webview
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Api:

    def say_hello(self, name):
        return f"Hello {name}"


def start_static_server(dist_path, port=8000):
    def server():
        os.chdir(dist_path)

        HTTPServer(
            ("127.0.0.1", port),
            SimpleHTTPRequestHandler
        ).serve_forever()

    threading.Thread(
        target=server,
        daemon=True
    ).start()


def run(url, debug=False):
    window = webview.create_window(
        "My Application",
        url,
        width=1400,
        height=900,
        js_api=Api()
    )

    webview.start(debug=debug)