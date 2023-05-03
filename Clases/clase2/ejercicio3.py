#!/usr/bin/python3
import argparse
import os
import sys


def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="archivo",
                        required=True, help="Nombre del archivo")

    parser.add_argument("-l", "--longitud", dest="longitudprom", required=False,  action="store_true",
                        help="Longitud promedio de palabras")

    return parser.parse_args()


def LeerArchivo(nombreArchivo, condicionLongitud):
    try:
        fd = os.open(nombreArchivo, os.O_RDONLY)
        # Contar cantidad de palabras
        texto = os.read(fd, 5000)
        palabras = texto.split()

        # Contar cantidad de lineas
        lines = texto.splitlines()

        # Longitud promedio - verificamos la condicion (True/False) para sacar la longitud promedio
        if condicionLongitud:
            caracteres_totales = 0
            numero_palabra = 0
            final = len(palabras)
            while True:
                caracteres_totales = caracteres_totales + \
                    len(palabras[numero_palabra])
                numero_palabra = numero_palabra + 1
                if numero_palabra == final:
                    break
            longitud_promedio = caracteres_totales/len(palabras)

            resultados = [len(palabras), len(lines), longitud_promedio]
        else:
            resultados = [len(palabras), len(lines), False]
        return resultados

    except OSError as error:
        with open('errors.log', mode='w+') as errorFile:
            print(error, file=errorFile)
            sys.stdout.write('\n')


if __name__ == "__main__":
    argumento = ArgsParse()
    nombreArchivo = argumento.archivo
    condicionLongitud = argumento.longitudprom

    resultados = LeerArchivo(nombreArchivo, condicionLongitud)
    cantidad_palabras = resultados[0]
    cantidad_lineas = resultados[1]
    longitud_prom = resultados[2]
    sys.stdout.write("\n")
    sys.stdout.write(
        "Cantidad de palabras que contiene el archivo: " + str(cantidad_palabras))
    sys.stdout.write("\n")
    sys.stdout.write(
        "Cantidad de lineas que contiene el archivo: " + str(cantidad_lineas))
    sys.stdout.write("\n")
    if condicionLongitud:
        sys.stdout.write(
            "Longitud promedio de palabras que contiene el archivo: " + str(longitud_prom))
        sys.stdout.write("\n")
