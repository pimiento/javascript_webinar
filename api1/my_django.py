#!/usr/bin/env python3
import io
import json
import http.server
import socketserver
from http import HTTPStatus
from datetime import datetime as dt

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        now = dt.now()
        data = json.dumps({
            "dt": now.strftime("%Y%m%d:%T"),
            "ts": int(now.timestamp())
        })
        s_data = io.BytesIO()
        s_data.write(data.encode("utf-8"))
        s_data.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.copyfile(s_data, self.wfile)

my_server = socketserver.TCPServer(("", 8000), MyHttpRequestHandler)

# Star the server
my_server.serve_forever()
