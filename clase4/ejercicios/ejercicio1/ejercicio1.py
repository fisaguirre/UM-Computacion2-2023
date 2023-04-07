#!/usr/bin/python3

"""
1- Escribir un programa en Python que comunique dos procesos. El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, contar la cantidad de palabras que contiene y mostrar ese número.

Usar sp , popen, os.
"""

import subprocess as sp
import os
import sys
import time
# Creamos el hijo, usando el programa hijo.py y usamos los pipes
hijo = sp.Popen(['./hijo.py'], stdin=sp.PIPE)

# padre lee el archivo y le escribe por la entrada del pipe la hij
fd = os.open('archivo.txt', os.O_RDONLY)
texto = (os.read(fd, 5000)).decode()
for line in texto:
    hijo.stdin.write(line.encode())

print("soy el padre: ", os.getpid())
# time.sleep(20)


# cerrar el pipe de entrada
hijo.stdin.close()
hijo.wait()
