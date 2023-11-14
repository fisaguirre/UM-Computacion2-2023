from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socketserver
import cgi
from PIL import Image
from io import BytesIO
import requests

class ImageHandler(BaseHTTPRequestHandler):
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
            url = "http://localhost:8081"
            factor_escala = 1.5  # Ajusta este valor según tus necesidades
            headers = {'Factor-Escala': str(factor_escala)}

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
    socketserver.TCPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(("localhost", 8080), ImageHandler)

    print("Primer servidor HTTP en puerto 8080")
    httpd.serve_forever()
