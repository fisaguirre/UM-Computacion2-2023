#!/usr/bin/python3
"""
FIFO con 4 hijos
"""

import time
import os

fifo_name = "mi_fifo"

try:
    os.mkfifo(fifo_name)  # crear FIFO
except FileExistsError:
    pass

# crear 4 procesos hijos
for i in range(4):
    pid = os.fork()
    if pid == 0:
        # proceso hijo
        with open(fifo_name, "r") as fifo:
            mensaje = fifo.read()
            print(f"Mensaje recibido por el hijo {i+1}:", mensaje)
            print("\n")

        with open(fifo_name, "w") as fifo:
            fifo.write(f"Hola desde el hijo {i+1}")
        fifo.close()
        os._exit(0)

# proceso padre
dato1 = 5
dato2 = 10
dato3 = 15
dato4 = 20
variable=str(dato1)+"-"+str(dato2)+"-"+str(dato3)+"-"+str(dato4)+","
with open(fifo_name, "w") as fifo:
    for i in range(4):
        fifo.write(str(variable))
fifo.close()

for i in range(4):
    with open(fifo_name, "r") as fifo:
        mensaje = fifo.read()
        print(f"Mensaje recibido por el padre desde el hijo {i+1}:", mensaje)
    fifo.close()

os.unlink(fifo_name)  # eliminar FIFO
