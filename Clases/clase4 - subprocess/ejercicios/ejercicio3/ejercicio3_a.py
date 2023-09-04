#!/usr/bin/python3
import subprocess as sp
import os
import sys
import time

"""
3- Verificar si el PIPE sigue existiendo cuendo el padre muere (termina el proceso), cuando el hijo muere 
[o cuendo mueren ambos]
$ ls -l /proc/[pid]/fd/
"""


def listar_pipes(pid):
    # listamos los pipes del proceso padre y los devolvemos para verificar si se encuentra el pipe del hijo
    p_ls = sp.Popen(['ls -la /proc/'+str(pid)+'/fd'],
                    shell=True, stdout=sp.PIPE)
    p_grep = sp.Popen(['grep', 'pipe'], stdin=p_ls.stdout, stdout=sp.PIPE)
    output, _ = p_grep.communicate()
    return output


def existe_pipes(output_padre, pipeHijo):
    # verificar si se encuentra el pipe padre-hijo
    pipes_padre_lineas = output_padre.splitlines()
    for i in range(len(pipes_padre_lineas)):
        if (pipes_padre_lineas[i].split()[-1] == pipeHijo):
            return True
    return False


print("Soy el padre -", os.getpid())
hijo1 = sp.Popen(['python3', 'hijo1.py'], stdin=sp.PIPE)

# enviamos mensaje al hijo por el pipe
mensaje = "Ustedes son mis hijos"
hijo1.stdin.write(mensaje.encode())


# listamos los pipes del proceso padre mientra el hijo sigue vivo
output_padre = listar_pipes(os.getpid())
print("pipes del padre: ")
print(output_padre.decode())

# listamos los pipes del proceso hijo
output_hijo = listar_pipes(hijo1.pid)

output_hijo = output_hijo
print("pipes del hijo: ")
print(output_hijo.decode())

pipes_hijo_lineas = output_hijo.splitlines()
pipeHijo = pipes_hijo_lineas[0].split()[-1]

# verificamos si esta el pipe en el padre
if (existe_pipes(output_padre, pipeHijo)):
    print("El pipe esta activo")
else:
    print("Muriò el pipe")
print(hijo1.returncode)

# esperamos que termine el proceso hijo
hijo1.stdin.close()
hijo1.wait()

if (hijo1.returncode == 0):
    print("---Muriò el hijo---")

    # listamos los pipes del proceso padre cuando muriò el hijo
    output_padre = listar_pipes(os.getpid())
    print("-----Pipes del padre-----")
    print(output_padre.decode())
    if (existe_pipes(output_padre, pipeHijo)):
        print("El pipe esta activo")
    else:
        print("Muriò el pipe")
    time.sleep(30)
