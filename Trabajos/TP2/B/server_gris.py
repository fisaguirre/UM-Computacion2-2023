import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socketserver
import cgi
from PIL import Image
from io import BytesIO
import requests


def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest="ip", required=True, help='Dirección IP')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, help='Puerto')
    parser.add_argument('-f', '--fac', dest="factor", required=True, type=int, help='Factor de escalado')
    parser.add_argument('-t', '--portb', dest="portB", required=True, type=int, help='Puerto server B')

    #parser.add_argument('-o', '--opt', dest="opcion", required=True, type=int, help='Opcion #A - #B - #C')
    return parser.parse_args()

class ImageHandler(BaseHTTPRequestHandler):
    factor_escala = 1.0  # Valor predeterminado
    puerto_serverB = 8081

    def do_POST(self):
        try:
            #analizar content-type, tupla (content type - dict de parametros)
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Tipo de contenido recibido: {content_type}")
            #content_length = int(self.headers['Content-Length'])
            
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
                    file_item = form_data['file']
                    img_data = file_item.file.read()
                    img = Image.open(BytesIO(img_data))

                    # Convertimos la imagen a escala de grises
                    img = img.convert('L')

                    # Enviamos la imagen al segundo servidor
                    self.enviar_a_segundo_servidor(img)

                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Imagen recibida y enviada correctamente del server gris.')
                    return

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: Formato de solicitud incorrecto.')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

    def enviar_a_segundo_servidor(self, img):
        try:
            url = "http://localhost:"+str(self.puerto_serverB)
            headers = {'Factor-Escala': str(self.factor_escala)}

            img_byte_array = BytesIO()
            img.save(img_byte_array, format='JPEG')
            img_bytes = img_byte_array.getvalue()
            #dict files para enviar en la solicitud
            files = {'file': ('imagen_recibida.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(url, files=files, headers=headers)

            if response.status_code == 200:
                print("Imagen enviada correctamente al segundo servidor.")
            else:
                print("Error al enviar la imagen al segundo servidor:", response.text)
        except Exception as e:
            print(f'Error al enviar la imagen al segundo servidor: {str(e)}')


if __name__ == "__main__":
    argumento = ArgsParse()
    socketserver.TCPServer.allow_reuse_address = True
    ImageHandler.factor_escala = int(argumento.factor)
    ImageHandler.puerto_serverB = int(argumento.portB)

    httpd = ThreadingHTTPServer((argumento.ip, argumento.port), ImageHandler)

    print("Primer servidor HTTP en puerto 8080")
    httpd.serve_forever()