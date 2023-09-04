#!/usr/bin/python3

import os
import time
import os

fifo_name = "mi_fifo"

# Creamos el archivo FIFO en el sistema de archivos
if not os.path.exists(fifo_name):
    os.mkfifo(fifo_name)

r, w = os.pipe()

pid = os.fork()

if pid == 0:
    # Estamos en el proceso hijo
    os.close(w)
    fifo = open(fifo_name, "r")
    while True:
        msg = fifo.readline().strip()
        if not msg:
            break
        print(f"Mensaje recibido en el hijo {os.getpid()}: {msg}")
    fifo.close()
    os.close(r)
else:
    # Estamos en el proceso padre
    os.close(r)
    fifo = open(fifo_name, "w")
    for i in range(5):
        #msg = f"Hola desde el padre al hijo {pid} - mensaje {i}"
        msg = f"Hola desde el padre al hijo {os.getpid()} - mensaje {i}"
        fifo.write(msg + "\n")
        fifo.flush()
    fifo.close()
    os.close(w)