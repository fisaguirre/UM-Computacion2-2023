#!/usr/bin/python3

import subprocess as sp
import os
import sys
import time

hijo1 = sp.Popen(['python3', 'hijo1.py'], stdin=sp.PIPE)
hijo2 = sp.Popen(['python3', 'hijo2.py'], stdin=sp.PIPE)
hijo3 = sp.Popen(['python3', 'hijo2.py'], stdin=sp.PIPE)

print("Soy el padre -", os.getpid())
mensaje = "Ustedes son mis hijos"


# cerrar el pipe de entrada
hijo1.stdin.write(mensaje.encode())
hijo2.stdin.write(mensaje.encode())
hijo3.stdin.write(mensaje.encode())


cp_ls = sp.Popen(['ls -la /proc/'+str(os.getpid()) +
                 '/fd'], shell=True, stdout=sp.PIPE)
cp_grep = sp.Popen(["grep", "pipe"], stdin=cp_ls.stdout)

"""
Se crea el pipe del padre con cada hijo, pero si corro el comando para ver los pipes por shell
no me muestra el pipe del primer proceso hijo que se corrio
"""
time.sleep(3)
pidhijo = os.getpid() + 1
print("el hijo: ", pidhijo)
print("el 1: ", cp_grep)


cp_ls2 = sp.Popen(['ls -la /proc/'+str(pidhijo) +
                   '/fd'], shell=True, stdout=sp.PIPE)
cp_grep2 = sp.Popen(["grep", "pipe"], stdin=cp_ls2.stdout)

# cerramos stdin para que no se quede esperando
hijo2.stdin.close()
hijo2.wait()
hijo1.stdin.close()
hijo1.wait()
hijo3.stdin.close()
hijo3.wait()

print("antes de morir")
time.sleep(3)
