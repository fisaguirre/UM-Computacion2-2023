#!/usr/bin/python3
import argparse
import os
import sys
# padre lee archivo, devuelve cantidad de lineas y las lineas
# se crea una lista de pipes para cada hijo con su padre
# padre le agrega a cada linea que va a enviar por el pipe un indice--> 1-"text"
# hijos leen, guardan el indice, hacen split y dan vuelta el texto
# hijos envian el indice y dado vuelta --> 1-"txet"


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


def invertir(lines, childPAmount):
    pipe_padre_hijo_r = []
    pipe_padre_hijo_w = []
    pipe_hijo_padre_r, pipe_hijo_padre_w = os.pipe()
    for i in range(childPAmount):
        r, w = os.pipe()
        pipe_padre_hijo_r.append(r)
        pipe_padre_hijo_w.append(w)

    for i in range(childPAmount):
        pid = os.fork()
        if (pid == 0):
            pipe = os.fdopen(pipe_padre_hijo_r[i])
            while True:
                linea_archivo = pipe.readline()
                print("I'm a children: ", os.getpid(),
                      " my father: ", os.getppid(), " - text: ", linea_archivo)
                # Si ya agarro una linea la invertimos, escribimos en el pipe y cerramos el hijo
                if (len(linea_archivo) != 0):
                    linea_archivo = str(linea_archivo)[:-1]  # delete \n
                    split_linea = linea_archivo.split("-")  # split line
                    linea_invertida = split_linea[1][::-1]
                    returnText = split_linea[0]+"-" + \
                        linea_invertida+"\n"
                    print("Hijo: ", i, " - devuelve:", returnText)
                    os.write(pipe_hijo_padre_w, returnText.encode("utf-8"))
                    pipe.close()
                    os._exit(0)

    # Por cada hijo enviamos una linea del archivo
    for i in range(childPAmount):
        lineaHijo = str(i)+"-"+lines[i]+"\n"
        os.write(pipe_padre_hijo_w[i], lineaHijo.encode("utf-8"))
    for i in range(childPAmount):
        os.wait()

    leido = os.read(pipe_hijo_padre_r, 1000).decode()
    splitLines = leido.split("\n")
    splitLines.sort()
    print("----------Texto devuelto por los hijos----------")
    for lineaInvertida in splitLines:
        if (len(lineaInvertida) != 0):
            lineaInvertida = lineaInvertida.split("-")
            print(lineaInvertida[1])


if __name__ == "__main__":
    argumento = ArgsParse()
    nombreArchivo = argumento.archivo
    lines, childPAmount = readFile(nombreArchivo)
    investedText = invertir(lines, childPAmount)
