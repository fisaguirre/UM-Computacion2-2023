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
    # listamos los pipes del proceso padre
    p_ls = sp.Popen(['ls -la /proc/'+str(pid)+'/fd'],
                    shell=True, stdout=sp.PIPE)
    p_grep = sp.Popen(['grep', 'pipe'], stdin=p_ls.stdout, stdout=sp.PIPE)
    output, _ = p_grep.communicate()
    return output


def existe_pipes(output_padre, pipeHijo):
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

pidhijo = os.getpid() + 1

# listamos los pipes del proceso padre
output_padre = listar_pipes(os.getpid())
print("pipes del padre: ")
print(output_padre.decode())

# listamos los pipes del proceso hijo
output_hijo = listar_pipes(pidhijo)

output_hijo = output_hijo
print("pipes del hijo: ")
print(output_hijo.decode())

pipes_hijo_lineas = output_hijo.splitlines()
pipeHijo = pipes_hijo_lineas[0].split()[-1]

# verificamos si esta el pipe en el padre
if (existe_pipes(output_padre, pipeHijo)):
    print("El pipe sigue activo")
else:
    print("Muriò el pipe")

# cerramos stdin para que no se quede esperando
hijo1.stdin.close()
hijo1.wait()

print("---Muriò el hijo---")

# listamos los pipes del proceso padre
output_padre = listar_pipes(os.getpid())
print("pipes del padre: ")
print(output_padre.decode())
if (existe_pipes(output_padre, pipeHijo)):
    print("El pipe sigue activo")
else:
    print("Muriò el pipe")
time.sleep(5)
