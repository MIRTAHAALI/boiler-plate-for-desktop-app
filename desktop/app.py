# # import os
# # import threading
# # import webview
# # from http.server import HTTPServer, SimpleHTTPRequestHandler

# # window = None


# # class Api:
# #     global window
# #     def say_hello(self, name):
# #         return f"Hello {name}"
    
# #     def open_file_dialog(self):
# #         # Define the file types you want to filter
# #         global window
# #         file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
        
# #         # Create the native open file dialog
# #         result = window.create_file_dialog(
# #     webview.OPEN_DIALOG,
# #     allow_multiple=True,
# #     file_types=(
# #         "Image Files (*.bmp;*.jpg;*.gif;*.png)",
# #         "All files (*.*)",
# #     ),
# # )
# #         print("Selected files:", result)
# #         return result


# # def start_static_server(dist_path, port=8000):
# #     def server():
# #         os.chdir(dist_path)

# #         HTTPServer(
# #             ("127.0.0.1", port),
# #             SimpleHTTPRequestHandler
# #         ).serve_forever()


# #     threading.Thread(
# #         target=server,
# #         daemon=True
# #     ).start()


# # def run(url, debug=False):
# #     global window
# #     window = webview.create_window(
# #         "My Application",
# #         url,
# #         width=1400,
# #         height=900,
# #         js_api=Api()
# #     )

# #     webview.start(debug=debug)



# import os
# import re
# import threading
# import urllib.parse
# import webview
# from http.server import HTTPServer, SimpleHTTPRequestHandler

# window = None


# class AppRequestHandler(SimpleHTTPRequestHandler):
#     """Serves the built React app normally, plus a /media endpoint
#     that streams arbitrary files from disk with HTTP Range support
#     (required for <video> seeking)."""

#     def do_GET(self):
#         parsed = urllib.parse.urlparse(self.path)

#         if parsed.path == "/media":
#             return self.serve_media(parsed)

#         # fallback to normal static file serving for the React build
#         return super().do_GET()

#     def serve_media(self, parsed):
#         qs = urllib.parse.parse_qs(parsed.query)
#         raw_path = qs.get("path", [None])[0]

#         if not raw_path:
#             self.send_error(400, "Missing 'path' query param")
#             return

#         file_path = urllib.parse.unquote(raw_path)

#         # NOTE: add your own validation here so this endpoint can't be
#         # abused to read arbitrary files if you ever expose it beyond
#         # localhost. e.g. check it's inside an allowed root folder.
#         if not os.path.isfile(file_path):
#             self.send_error(404, "File not found")
#             return

#         file_size = os.path.getsize(file_path)
#         range_header = self.headers.get("Range")

#         if range_header:
#             match = re.match(r"bytes=(\d+)-(\d*)", range_header)
#             start = int(match.group(1))
#             end = int(match.group(2)) if match.group(2) else file_size - 1
#             end = min(end, file_size - 1)
#             length = end - start + 1

#             self.send_response(206)
#             self.send_header("Content-Type", "video/mp4")
#             self.send_header("Accept-Ranges", "bytes")
#             self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
#             self.send_header("Content-Length", str(length))
#             self.end_headers()

#             with open(file_path, "rb") as f:
#                 f.seek(start)
#                 remaining = length
#                 chunk_size = 1024 * 1024
#                 while remaining > 0:
#                     chunk = f.read(min(chunk_size, remaining))
#                     if not chunk:
#                         break
#                     self.wfile.write(chunk)
#                     remaining -= len(chunk)
#         else:
#             self.send_response(200)
#             self.send_header("Content-Type", "video/mp4")
#             self.send_header("Accept-Ranges", "bytes")
#             self.send_header("Content-Length", str(file_size))
#             self.end_headers()
#             with open(file_path, "rb") as f:
#                 self.wfile.write(f.read())


# class Api:
#     def say_hello(self, name):
#         return f"Hello {name}"

#     def open_file_dialog(self):
#         global window
#         result = window.create_file_dialog(
#             webview.OPEN_DIALOG,
#             allow_multiple=True,
#             file_types=(
#                 "Video Files (*.mp4;*.mkv;*.avi)",
#                 "All files (*.*)",
#             ),
#         )
#         print("Selected files:", result)
#         return result


# def start_static_server(dist_path, port=8000):
#     def server():
#         os.chdir(dist_path)
#         HTTPServer(("127.0.0.1", port), AppRequestHandler).serve_forever()
#         print(f"Static server started at http://127.0.0.1:{port}")

#     print(f"Starting static server at {dist_path} on port {port}...")
#     threading.Thread(target=server, daemon=True).start()


# def run(url, debug=False):
#     print(f"Starting webview with URL: {url}")
#     global window
#     window = webview.create_window(
#         "My Application",
#         url,
#         width=1400,
#         height=900,
#         js_api=Api(),
#     )
#     webview.start(debug=debug)


import os
import re
import threading
import urllib.parse
import webview
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler

window = None


class MediaRequestHandler(SimpleHTTPRequestHandler):
    """Handles /media?path=... for streaming local video files with Range support."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/media":
            return self.serve_media(parsed)
        return super().do_GET()

    def serve_media(self, parsed):
        qs = urllib.parse.parse_qs(parsed.query)
        raw_path = qs.get("path", [None])[0]
        if not raw_path:
            self.send_error(400, "Missing 'path' query param")
            return

        file_path = urllib.parse.unquote(raw_path)
        if not os.path.isfile(file_path):
            self.send_error(404, "File not found")
            return

        file_size = os.path.getsize(file_path)
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1

            self.send_response(206)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(length))
            self.end_headers()

            with open(file_path, "rb") as f:
                f.seek(start)
                remaining = length
                chunk_size = 1024 * 1024
                while remaining > 0:
                    chunk = f.read(min(chunk_size, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(file_size))
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())


class Api:
    def say_hello(self, name):
        return f"Hello {name}"

    def open_file_dialog(self):
        global window
        result = window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=True,
            file_types=("Video Files (*.mp4;*.mkv;*.avi)", "All files (*.*)"),
        )
        print("Selected files:", result)
        return result


def start_media_server(port=8000):
    """Use this in DEV mode — only serves /media, React itself comes from Vite."""
    def server():
        try:
            ThreadingHTTPServer(("127.0.0.1", port), MediaRequestHandler).serve_forever()
        except Exception as e:
            print("Media server failed to start:", e)

    threading.Thread(target=server, daemon=True).start()


def start_static_server(dist_path, port=8000):
    """Use this in BUILD mode — serves the built React app AND /media on the same port."""
    def server():
        try:
            os.chdir(dist_path)
            ThreadingHTTPServer(("127.0.0.1", port), MediaRequestHandler).serve_forever()
        except Exception as e:
            print("Static server failed to start:", e)

    threading.Thread(target=server, daemon=True).start()


def run(url, debug=False):
    global window
    window = webview.create_window(
        "My Application", url, width=1400, height=900, js_api=Api()
    )
    webview.start(debug=debug)