#!/usr/bin/python3
import sys
import getopt
"""
2- Escribir un programa en Python que acepte dos argumentos de línea de comando: una cadena de texto,
un número entero.
El programa debe imprimir una repetición de la cadena de texto tantas veces como el número entero.
"""

(opt, arg) = getopt.getopt(sys.argv[1:], 's:n:', ['string=', 'number='])

texto = 0
numero = 0


for op, ar in opt:
    if (op in ['-s', '--string']):
        sys.stdout.write("Cadena de texto: "+ar)
        sys.stdout.write("\n")
        texto = ar
    elif (op in ['-n', '--number']):
        sys.stdout.write("Cantidad de repeticiones: "+ar)
        sys.stdout.write("\n")
        numero = ar

sys.stdout.write("\n")
for i in range(int(numero)):
    sys.stdout.write(str(i+1)+": "+texto)
    sys.stdout.write("\n")
