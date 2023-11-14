#!/usr/bin/python3
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
from io import BytesIO
import cgi

def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest="ip", required=True, help='Dirección IP de escucha')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, help='Puerto de escucha')
    return parser.parse_args()

class ImageReceiverHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Tipo de contenido recibido: {content_type}")

            #content_length = int(self.headers['Content-Length'])
            #img_data = self.rfile.read(content_length)
            
            form_data = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type']}
                )
            
            file_item = form_data['file']
            img_data = file_item.file.read()
            # Cargamos la imagen recibida
            img = Image.open(BytesIO(img_data))
            

            # Redimensionamos la imagen según el factor de escala
            factor_escala = float(self.headers['Factor-Escala'])
            print("factor: ",factor_escala)
            new_width = int(img.width / factor_escala)
            new_height = int(img.height / factor_escala)
            img_resized = img.resize((new_width, new_height))

            # Enviamos la imagen redimensionada de vuelta
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()

            # Convertimos la imagen redimensionada a bytes y la enviamos
            img_byte_array = BytesIO()
            img_resized.save(img_byte_array, format='JPEG')
            img_bytes = img_byte_array.getvalue()
            self.wfile.write(img_bytes)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

if __name__ == "__main__":
    argumento = ArgsParse()
    server_address = (argumento.ip, argumento.port)

    httpd = HTTPServer(server_address, ImageReceiverHandler)

    print("Servidor  en puerto: ",argumento.port)
    httpd.serve_forever()
