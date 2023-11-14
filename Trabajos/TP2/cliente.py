#!/usr/bin/python3

import argparse
import requests

def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest="ip", required=True, help='Dirección IP destino')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, help='Puerto destino')
    parser.add_argument('-f', '--file', dest="file", required=True, type=str, help='Nombre imagen con extension')
    parser.add_argument('-e', '--factor', dest="factor", required=False, type=float, help='Factor de escala')
    return parser.parse_args()

def enviar_imagen_jpeg(ip, port, imagen, factor):
    url = "http://"+ip+":"+str(port)
    if(factor):
        headers = {'Factor-Escala': str(factor)}
    file_path = imagen

    with open(file_path, "rb") as file:
        files = {'file': ('imagen.jpg', file, 'image/jpeg')}
        if(factor):
            response = requests.post(url, files=files, headers=headers)
        else:
            response = requests.post(url, files=files)

        if response.status_code == 200:
            # Guardamos la imagen recibida del servidor
            with open("imagen_gris_reducida.jpg", "wb") as output_file:
                output_file.write(response.content)
                print("Imagen recibida y guardada correctamente.")
        else:
            print("Error en la solicitud al servidor:", response.text)

if __name__ == "__main__":
    argumentos = ArgsParse()
   
    enviar_imagen_jpeg(argumentos.ip, argumentos.port, argumentos.file, argumentos.factor)
