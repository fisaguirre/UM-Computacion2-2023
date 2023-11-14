import requests

def enviar_imagen_jpeg():
    url = "http://localhost:8080"
    file_path = "imagen.jpg"

    with open(file_path, "rb") as file:
        files = {'file': ('imagen.jpg', file, 'image/jpeg')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            # Guardamos la imagen recibida del servidor
            with open("imagen_recibida.jpg", "wb") as output_file:
                output_file.write(response.content)
                print("Imagen recibida y guardada correctamente.")
        else:
            print("Error en la solicitud al servidor:", response.text)

if __name__ == "__main__":
    enviar_imagen_jpeg()
