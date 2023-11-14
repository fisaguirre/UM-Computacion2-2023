#!/usr/bin/python3
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import multiprocessing
import socket
import socketserver
import cgi
import threading
from time import sleep
from urllib.parse import parse_qs
from PIL import Image
from io import BytesIO
import requests
import queue


cola_compartida = multiprocessing.Queue()

def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest="ip", required=True, help='Dirección IP de escucha')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, help='Puerto de escucha')
    parser.add_argument('-f', '--fac', dest="factor", required=True, type=float, help='Factor de escalado')
    parser.add_argument('-t', '--portb', dest="portB", required=True, type=int, help='Puerto destino server B')
    return parser.parse_args()

class ImageHandler(BaseHTTPRequestHandler):
    factor_escala = 1.0  # Valor predeterminado
    puerto_serverB = 8081 # puerto predeterminado

    def log_message(self, format, *args):
        client_host, client_port = self.client_address
        print(f"Cliente {client_host}:{client_port} - {format % args}")

    def handle(self):
        client_host, client_port = self.client_address
        print(f"Se ha conectado el cliente {client_host}:{client_port}")
        super().handle()

    def do_POST(self):
        try:
            #analizar content-type, tupla (content type - dict de parametros)
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Tipo de contenido recibido: {content_type}")
           
            if content_type == 'multipart/form-data':
                #vemos los datos del formulario y lo guardamos en form_data
                form_data = cgi.FieldStorage(
                    #rfile->flujo de entrada de la solicitud
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type']}
                )

                if 'file' in form_data:
                    if(self.headers['Factor-Escala']):
                        self.factor_escala = self.headers['Factor-Escala']
                    #factor_escala = float(self.headers['Factor-Escala'])

                    proceso_hijo = multiprocessing.Process(target=convertirGris, args=(form_data, cola_compartida))
                    proceso_hijo.start()

                    img = cola_compartida.get()
                    proceso_hijo.join()
                    # Enviamos la imagen al segundo servidor
                    imagenGrisReducida = reducirFactorEscalaServerB(self.puerto_serverB, self.factor_escala, img)

                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.wfile.write(imagenGrisReducida)
                    #self.server.shutdown()

                    return
                    
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: Formato de solicitud incorrecto.')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())


def convertirGris(form_data,cola_compartida):
    file_item = form_data['file']
    img_data = file_item.file.read()
    img = Image.open(BytesIO(img_data))

    # Convertimos la imagen a escala de grises
    img = img.convert('L')
    cola_compartida.put(img)
     
def reducirFactorEscalaServerB(puerto_serverB, factor_escala, img):
    try:
            url = "http://localhost:"+str(puerto_serverB)
            headers = {'Factor-Escala': str(factor_escala)}

            img_byte_array = BytesIO()
            img.save(img_byte_array, format='JPEG')
            img_bytes = img_byte_array.getvalue()
            #dict files para enviar en la solicitud
            files = {'file': ('imagen_recibida.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(url, files=files, headers=headers)

            if response.status_code == 200:
                print("Imagen enviada correctamente al segundo servidor.")
                return response.content
            else:
                print("Error al enviar la imagen al segundo servidor:", response.text)
    except Exception as e:
            print(f'Error al enviar la imagen al segundo servidor: {str(e)}')
            
if __name__ == "__main__":
    argumento = ArgsParse()
    socketserver.TCPServer.allow_reuse_address = True
    
    ImageHandler.factor_escala = float(argumento.factor)
    ImageHandler.puerto_serverB = int(argumento.portB)

    httpd = ThreadingHTTPServer((argumento.ip, argumento.port), ImageHandler)

    print("Servidor HTTP en puerto: ", argumento.port)
    httpd.serve_forever()

    #httpd.server_close()