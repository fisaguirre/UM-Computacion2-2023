#!/usr/bin/python3
import sys

"""
1- Escribir un programa en Python que acepte un número de argumento entero positivo n y genere una lista de los n primeros números impares. El programa debe imprimir la lista resultante en la salida estandar.
n=5
Salida: 1,3,5,7,9
"""
if (len(sys.argv) == 2):
    cantidad_impares = sys.argv[1]
else:
    cantidad_impares = sys.argv[2]

impares = 1
for i in range(int(cantidad_impares)):
    sys.stdout.write(str(impares))
    sys.stdout.write("\n")
    impares = impares + 2
