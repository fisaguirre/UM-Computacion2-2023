"""
Realizar un programa que implemente un servidor UDP usando socketserver.
El servidor puede ser un servidor de mayúsculas, un codificador en rot13 o cualquier otra tarea simple.
Se debe implementar concurrencia usanfo forking o threading.
"""

import socketserver
import threading

def mayus(s):
    msg = s
    return msg.decode().upper()

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        print(data.decode())

        print(f"Conexion establecida con {self.client_address[0]}")
        print(f"{self.client_address[0]} dijo: {mayus(data)}")

if __name__ == '__main__':
    
    HOST, PORT = "localhost", 5000
    with socketserver.ThreadingUDPServer((HOST, PORT), ThreadedUDPRequestHandler) as server:
        server.serve_forever()