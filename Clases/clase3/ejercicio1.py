#!/usr/bin/python3

import os
import argparse
import sys
import time
"""
Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar relizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.
"""


def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", dest="numero",
                        required=True, help="Numero")
    parser.add_argument("-f", "--fork", dest="fork",
                        required=False,  action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    argumento = ArgsParse()
    numero = int(argumento.numero)
    proceso = argumento.fork

    sys.stdout.write("\n"+"Soy el padre: "+str(os.getpid()))
    raizPositiva = pow(numero, 1/2)
    sys.stdout.write("\n"+"La raiz positiva de " +
                     str(numero)+" es: "+str(raizPositiva)+"\n")

    if (proceso):
        process = os.fork()
        if process == 0:
            sys.stdout.write("\n")
            sys.stdout.write("Soy el hijo "+str(os.getpid()) +
                             " y mi padre es: "+str(os.getppid()))
            sys.stdout.write("\n")
            raizNegativa = pow(numero, 1/(-2))
            sys.stdout.write("La raiz negativa de " +
                             str(numero)+" es: "+str(raizNegativa)+"\n")
    else:
        sys.stdout.write("\n"+"Soy un padre sin hijos")
        sys.stdout.write("\n"+"Soy el padre: "+str(os.getpid()))
        raizNegativa = pow(numero, 1/(-2))
        sys.stdout.write("\n"+"La raiz negativa de " +
                         str(numero)+" es: "+str(raizNegativa)+"\n")
