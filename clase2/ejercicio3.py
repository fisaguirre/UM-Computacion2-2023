#!/usr/bin/python3
import getopt
import argparse
import os
import sys

"""
Escribir un programa en Python que acepte argumentos de línea de comando para leer un archivo de texto (pasado como argumento). El programa debe contar el número de palabras y líneas del archivo e imprimirlas en la salida estándar. Además el programa debe aceptar una opción para imprimir la longitud promedio de las palabras del archivo. Esta última opción no debe ser obligatoria. Si hubiese errores deben guardarse el un archivo cuyo nombre será "errors.log" usando la redirección de la salida de error.

La opcion no es obligatoria en el sentido de que puedo o no ponerla en el bash, pero debo programarlo.
"""


def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="archivo",
                        required=True, help="Nombre del archivo")

    parser.add_argument("-l", "--longitud", dest="longitudprom", required=False, nargs="?",
                        help="Longitud promedio de palabras")

    return parser.parse_args()


def LeerArchivo(nombreArchivo):
    fd = os.open(nombreArchivo, os.O_RDONLY)
    # Contar cantidad de palabras
    texto = os.read(fd, 5000)
    palabras = texto.split()

    # Contar cantidad de lineas
    lines = texto.splitlines()

    # Longitud promedio
    caracteres_totales = 0
    numero_palabra = 0
    final = len(palabras)
    while True:
        caracteres_totales = caracteres_totales + len(palabras[numero_palabra])
        numero_palabra = numero_palabra + 1
        if numero_palabra == final:
            break
    longitud_promedio = caracteres_totales/len(palabras)

    lista = [len(palabras), len(lines), longitud_promedio]
    return lista


if __name__ == "__main__":
    argumento = ArgsParse()
    nombreArchivo = argumento.archivo
    lista = LeerArchivo(nombreArchivo)
    cantidad_palabras = lista[0]
    cantidad_lineas = lista[1]
    longitud_prom = lista[2]
    sys.stdout.write("\n")
    sys.stdout.write(
        "Cantidad de palabras que contiene el archivo: " + str(cantidad_palabras))
    sys.stdout.write("\n")
    sys.stdout.write(
        "Cantidad de lineas que contiene el archivo: " + str(cantidad_lineas))
    sys.stdout.write("\n")
    sys.stdout.write(
        "Longitud promedio de palabras que contiene el archivo: " + str(longitud_prom))
    sys.stdout.write("\n")
