import os
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import websockets
import asyncio

activeSockets = []


data = {"lat":-1,
        "long":-1,
        "alt":-1,
        "temp":-1,
        "hum":-1,
        "heading":-1}

async def sendWebsockets():
    print("sending to", len(activeSockets), "sockets")
    for sock in activeSockets:
        
        await sock.send(str(data))

def serialListener():
    while True:
        time.sleep(0.5)
        data["long"] = random.random()
        data["lat"] = random.random()
        asyncio.run(sendWebsockets())

async def handle_connection(websocket, path):
    activeSockets.append(websocket)
    print("WebSocket connection established and added to the list")
    while websocket.open:
        pass
    print("websocket was closed")
    activeSockets.remove(websocket)

async def websockets_server():
    print("starting websocket listener")
    
    async with websockets.serve(handle_connection, "localhost", 8765, ping_interval=2, ping_timeout=2):
        await asyncio.Future()
    

class Server(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(data).replace("'", '"').encode("utf-8"))
        else:
            SimpleHTTPRequestHandler.do_GET(self)

def http_server():
    print("stargin server")
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, Server)
    httpd.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=http_server).start()
    threading.Thread(target=serialListener).start()
    asyncio.run(websockets_server())


