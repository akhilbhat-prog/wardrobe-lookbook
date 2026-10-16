"""Desktop launcher for the Wardrobe Lookbook.

Runs the Flask app on a background thread bound to a free localhost port, then opens it in a
native window (pywebview / WebView2) -- no browser, no console. Closing the window exits the
process cleanly (the Flask thread is a daemon).

Usage (dev):   python desktop.py
Packaged:      launched as WardrobeLookbook.exe
"""
import socket
import threading
import time
import urllib.request

import webview

import app as flask_app


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _serve(port):
    # Production-ish: no debug, no reloader (reloader would fork a second process).
    flask_app.app.run(host="127.0.0.1", port=port, threaded=True,
                      debug=False, use_reloader=False)


def _wait_until_up(url, timeout=15.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.1)
    return False


def main():
    port = _free_port()
    threading.Thread(target=_serve, args=(port,), daemon=True).start()
    url = f"http://127.0.0.1:{port}/"
    _wait_until_up(url)
    webview.create_window(
        "Wardrobe Lookbook",
        url,
        width=1240,
        height=840,
        min_size=(900, 600),
    )
    webview.start()  # blocks until the window is closed


if __name__ == "__main__":
    main()
