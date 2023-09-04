#!/usr/bin/python3
"""
1- Escribir un programa que realice la multiplicación de dos matrices de 2x2. Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.
"""
import os
import sys
import time
fifo_name = "mi_fifo23"
dato1 = 1
dato2 = 2
dato3 = 3
dato4 = 4

dato5 = 5
dato6 = 6
dato7 = 7
dato8 = 8

indice_a = "v1"
indice_b = "v2"
indice_c = "v3"
indice_d = "v4"
valor_indice_a = indice_a+"-"+str(dato1) + "-" + str(dato2) + "-" + \
    str(dato5) + "-" + str(dato7)
valor_indice_b = indice_b+"-"+str(dato1) + "-" + str(dato2) + "-" + \
    str(dato6) + "-" + str(dato8)
valor_indice_c = indice_c+"-" + \
    str(dato3) + "-" + str(dato4) + "-" + str(dato5) + "-" + str(dato7)
valor_indice_d = indice_d+"-"+str(dato3) + "-" + str(dato4) + "-" + \
    str(dato6) + "-" + str(dato8)

lista_valores = [valor_indice_a, valor_indice_b,
                 valor_indice_c, valor_indice_d]
try:
    os.mkfifo(fifo_name)  # crear FIFO
except FileExistsError:
    pass

# crear 4 procesos hijos
for i in range(4):
    pid = os.fork()
    if pid == 0:
        resultado = 0
        indice_matriz = ""
        index = str(i)
        matriz_hijo = lista_valores[i]
        print('Soy el hijo ', i+1)
        split_values = matriz_hijo.split("-")
        result = str(int(split_values[1])*int(split_values[3]) +
                     int(split_values[2])*int(split_values[4]))

        indexResult = index+"-"+result
        pipeWriteChildrenToFather = os.open(
            fifo_name, os.O_WRONLY | os.O_APPEND)
        print("Enviando resultado del hijo al padre - indice: ",
              index, " - valor: ", indexResult)
        os.write(pipeWriteChildrenToFather,
                 (indexResult+"\n").encode("utf-8"))

        os.close(pipeWriteChildrenToFather)

        os._exit(0)

nueva_matriz = []

pipeReadFatherMatriz = open(fifo_name, 'r')
for i in range(4):
    os.wait()

for line in pipeReadFatherMatriz:
    line = str(line)[:-1]  # delete \n
    spliteado = line.split("-")
    nueva_matriz.insert(int(spliteado[0]), spliteado[1])

pipeReadFatherMatriz.close()

print("matriz: ", nueva_matriz)
# os.unlink(fifo_name)  # eliminar FIFO
