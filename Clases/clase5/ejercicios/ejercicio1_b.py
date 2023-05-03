#!/usr/bin/python3
"""
1- Escribir un programa que realice la multiplicación de dos matrices de 2x2. Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.
"""
import os
import sys
import time
fifo_name = "mi_fifo"

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
        index = str(i+1)
        pipeReadChildren = open(fifo_name, 'r', 300)
        for line in pipeReadChildren:
            # print('Soy el hijo ', i, ' y leo: ', line)
            """
            print("linea: ", line, " - indice: ", i+1, " - primero: ",
                  line[0], " - segundo: ", line[1], " - ultimo: ", line[-3])
            """
            if (line[0] == "v" and line[1] == index and line[-1] == "\n"):
                print('Soy el hijo ', i+1, ' y leo: ', line)
                mis_valores = line
                mis_valores = str(mis_valores)[:-1]  # delete \n
                split_values = mis_valores.split("-")
                # print("values are: ", split_values)
                result = str(int(split_values[1])*int(split_values[3]) +
                             int(split_values[2])*int(split_values[4]))

                # print("result from child: ", result)
                indexResult = "r"+index+"-"+result
                # print("type of indexREsult: ", type(indexResult))
                #pipeWriteChildrenToFather = os.open(fifo_name, os.O_WRONLY)
                pipeWriteChildrenToFather = os.open(fifo_name, os.O_WRONLY)
                print("Enviando resultado del hijo al padre - indice: ",
                      index, " - valor: ", indexResult)
                if (i == 0):
                    time.sleep(2)
                if (i == 1):
                    time.sleep(4)
                if (i == 2):
                    time.sleep(6)

                os.write(pipeWriteChildrenToFather,
                         ("\n"+indexResult+"\n").encode("utf-8"))
                pipeReadChildren.close()

                os.close(pipeWriteChildrenToFather)

                os._exit(0)

        print("se murio el hijo y su resultado es: ", resultado)


# proceso padre
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
# lista_valores = valor_indice_a+valor_indice_b+valor_indice_c+valor_indice_d
"""
tamaño_bytes = sys.getsizeof(valor_indice_a)
print(f"El tamaño en bytes de la aaaa es: {tamaño_bytes}")
"""

pipeWriteFather = os.open(fifo_name, os.O_WRONLY)
indice = 1
for valor in lista_valores:
    print("Enviando valores de la matriz del padre al hijo: ", valor)
    os.write(pipeWriteFather, (valor+"\n").encode("utf-8"))


nueva_matriz = []

pipeReadFatherMatriz = open(fifo_name, 'r')
time.sleep(3)

for line in pipeReadFatherMatriz:
    print("line is: ", line)
    nueva_matriz.append(line)

pipeReadFatherMatriz.close()
print("matriz: ", nueva_matriz)

"""
pipeReadFatherMatriz = os.open(fifo_name, os.O_RDONLY)
time.sleep(3)
print("type of only: ", type(pipeReadFatherMatriz))

for line in str(pipeReadFatherMatriz):
    print(f"Mensaje recibido por el padre desde el hijo {i+1}:", line)
    nueva_matriz.append(line)

pipeReadFatherMatriz.close()
"""
# os.unlink(fifo_name)  # eliminar FIFO
