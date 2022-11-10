#!/usr/bin/env python3
import json
import datetime as dt
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.websocket import WebSocketHandler
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler

define('port', default=8888, help='port to listen on', type=int)
SOCKETS = []
MESSAGES = []


class MainHandler(RequestHandler):
    def get(self):
        self.render('index.html')

class WSChatHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        global SOCKETS
        print('Socket opened')
        for m in MESSAGES:
            self.write_message(m)
        SOCKETS.append(self)

    def on_message(self, message):
        global MESSAGES
        data = json.loads(message)
        data["time"] = dt.datetime.now().strftime("%Y-%d-%m %T")
        message = json.dumps(data)
        MESSAGES.append(message)
        MESSAGES = MESSAGES[:10]
        if data['type'] == 'message':
            for s in SOCKETS:
                s.write_message(message)

    def on_close(self):
        print('Websocket closed')
        if self in SOCKETS:
            SOCKETS.remove(self)


def main():
    """Construct and serve the tornado application."""
    parse_command_line()

    APP = Application(
        handlers=[
            (r'/', MainHandler),
            (r'/chat', WSChatHandler),
        ],
        template_path=".",
        static_path = "./static/"
    )
    http_server = HTTPServer(APP)
    http_server.listen(options.port, address='0.0.0.0')
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
