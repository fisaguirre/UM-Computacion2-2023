#!/usr/bin/python3
import sys
import os
# leemos la entrada del pipe
i = 0
print("soy el hijo: ", os.getpid())
for line in sys.stdin:
    i = i + 1
    cantidad_palabras = len(line.split())
    # mandamos por la salida del pipe la cantidad
    sys.stdout.write("Linea "+str(i)+": " +
                     str(cantidad_palabras) + " palabras"+"\n")
