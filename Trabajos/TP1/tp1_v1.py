#!/usr/bin/python3
import argparse
import os
import sys
import time

# padre lee archivo, devuelve cantidad de lineas y las lineas
# se crea una lista de pipes para cada hijo con su padre
# padre le agrega a cada linea que va a enviar por el pipe un indice--> 1-"text"
# hijos leen, guardan el indice, hacen split y dan vuelta el texto
# hijos envian el indice y dado vuelta --> 1-"txet"
# padre lee todo y hace split en "\n"
# padre hace split de nuevo segun "-"
# padre hace un lista.insert(indice,texto) y luego muestra por pantalla todas las lineas

# ----------------------------1 PIPE POR CADA HIJO----------------------------


def ArgsParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="archivo",
                        required=True, help="Nombre del archivo")
    return parser.parse_args()


def readFile(nombreArchivo):
    try:
        fdr = open(nombreArchivo, 'r')
        lines = fdr.readlines()
        childPAmount = len(lines)
        fdr.close()
        return lines, childPAmount

    except OSError as error:
        with open('errors.log', mode='w+') as errorFile:
            print(error, file=errorFile)
            sys.stdout.write('\n')


def invest(lines, childPAmount):
    rPipeList = []
    wPipeList = []
    r0, w0 = os.pipe()
    for i in range(childPAmount):
        r, w = os.pipe()
        rPipeList.append(r)
        wPipeList.append(w)

    for i in range(childPAmount):
        pid = os.fork()
        if (pid == 0):
            pipe = os.fdopen(rPipeList[i])
            while True:
                leido = pipe.readline()
                print("I'm a children: ", os.getpid(),
                      " my father: ", os.getppid(), " - text: ", leido)
                # Si ya agarro una linea la invertimos, escribimos en el pipe y cerramos el hijo
                if (len(leido) != 0):
                    leido = str(leido)[:-1]  # delete \n
                    leido_split = leido.split("-")  # split line
                    investedText = leido_split[1][::-1]
                    returnText = leido_split[0]+"-" + \
                        investedText+"\n"
                    print("Hijo: ", i, " - devuelve:", returnText)
                    os.write(w0, returnText.encode("utf-8"))
                    time.sleep(30)
                    pipe.close()
                    os._exit(0)
                # time.sleep(3)

    # Por cada hijo enviamos una linea del archivo
    print(os.getpid(), " - Soy el padre enviando lineas: ")
    for i in range(childPAmount):
        texto = str(i)+"-"+lines[i]+"\n"
        os.write(wPipeList[i], texto.encode("utf-8"))
    for i in range(childPAmount):
        os.wait()
    # Leemos por el pipe las lineas invertidas, hacemos decode, split y retornamos para luego mostrarlas
    while True:
        # child must read 1 linea not more
        leido = os.read(r0, 1000)
        leido = leido.decode()
        splitLines = leido.split("\n")
        return splitLines
        # time.sleep(3)


def showInvestedText(returnText):
    lista = []
    for text in returnText:
        if (len(text) != 0):
            text = text.split("-")
            lista.insert(int(text[0]), text[1])

    print("----------Texto devuelto por los hijos----------")
    for valor in lista:
        print(valor)


if __name__ == "__main__":
    argumento = ArgsParse()
    nombreArchivo = argumento.archivo
    lines, childPAmount = readFile(nombreArchivo)
    investedText = invest(lines, childPAmount)
    showInvestedText(investedText)
