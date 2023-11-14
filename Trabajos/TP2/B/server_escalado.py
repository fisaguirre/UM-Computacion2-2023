import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
from io import BytesIO
import os
import cgi

def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest="ip", required=True, help='Dirección IP')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, help='Puerto')
    return parser.parse_args()

class ImageReceiverHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Tipo de contenido recibido: {content_type}")

            content_length = int(self.headers['Content-Length'])
            print("lengt: ", content_length)
            #img_data = self.rfile.read(content_length)
            
            form_data = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type']}
                )
            if 'file' in form_data:
                print("esta adentro")
            print(form_data)

            file_item = form_data['file']
            img_data = file_item.file.read()
            # Cargamos la imagen recibida
            img = Image.open(BytesIO(img_data))

            # Convertimos la imagen a escala de grises
            #img = img.convert('L')
            # Redimensionamos la imagen según el factor de escala proporcionado por el primer servidor
            factor_escala = float(self.headers['Factor-Escala'])
            print("factor: ",factor_escala)
            new_width = int(img.width * factor_escala)
            new_height = int(img.height * factor_escala)
            img_resized = img.resize((new_width, new_height))

            # Guardamos la imagen redimensionada
            img_resized.save("imagen_recibida_redimensionada.jpg")

            # Enviamos la imagen redimensionada de vuelta al primer servidor
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()

            # Convertimos la imagen redimensionada a bytes y la enviamos al primer servidor
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

    print("Segundo servidor de Recepción en puerto: ",argumento.port)
    httpd.serve_forever()
