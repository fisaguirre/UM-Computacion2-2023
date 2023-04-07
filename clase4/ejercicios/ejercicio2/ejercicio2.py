#!/usr/bin/python3
import subprocess as sp
import os
import sys
import time
"""
2- Verificar si es posible que dos procesos hijos (o nieto) lean el PIPE del padre.
"""
"""
En este programa se crean 2 pipes por cada hijo, no se usa el mismo pipe para los 2.
"""

"""
tuberia = sp.PIPE
hijo1 = sp.Popen(['python3', 'hijo1.py'], stdin=tuberia)
hijo2 = sp.Popen(['python3', 'hijo2.py'], stdin=tuberia)
"""
hijo1 = sp.Popen(['python3', 'hijo1.py'], stdin=sp.PIPE)
hijo2 = sp.Popen(['python3', 'hijo2.py'], stdin=sp.PIPE)

print("Soy el padre -", os.getpid())
mensaje = "Ustedes son mis hijos"


# cerrar el pipe de entrada
hijo1.stdin.write(mensaje.encode())
hijo2.stdin.write(mensaje.encode())


# cerramos stdin para que no se quede esperando
hijo2.stdin.close()
hijo2.wait()
hijo1.stdin.close()
hijo1.wait()
print("antes de morir")
time.sleep(100)
