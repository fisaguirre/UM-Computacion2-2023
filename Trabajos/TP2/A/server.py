from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socketserver
import cgi
from PIL import Image
from io import BytesIO

class ImageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Tipo de contenido recibido: {content_type}")

            if content_type == 'multipart/form-data':
                form_data = cgi.FieldStorage(
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

                    # Guardamos la imagen convertida en escala de grises
                    #img.save("imagen_recibida_gris.jpg")

                    # Enviamos la imagen de vuelta al cliente
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    
                    # Convertimos la imagen de Pillow a bytes y la enviamos al cliente
                    img_byte_array = BytesIO()
                    img.save(img_byte_array, format='JPEG')
                    img_bytes = img_byte_array.getvalue()
                    self.wfile.write(img_bytes)
                    return

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: Formato de solicitud incorrecto.')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(("localhost", 8080), ImageHandler)

    print("Servidor HTTP en puerto 8080")
    httpd.serve_forever()
