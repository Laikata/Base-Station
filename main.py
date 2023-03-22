import os
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time


data = {"lat":-1,
        "long":-1,
        "alt":-1,
        "temp":-1,
        "hum":-1,
        "heading":-1}

def serialListener():
    while True:
        time.sleep(0.5)
        data["long"] = random.random()
        data["lat"] = random.random()



class Server(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(data).replace("'", '"').encode("utf-8"))
        else:
            SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':

    serialThread = threading.Thread(target=serialListener)
    serialThread.start()

    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, Server)
    httpd.serve_forever()

