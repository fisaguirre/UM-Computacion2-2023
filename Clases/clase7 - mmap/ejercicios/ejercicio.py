import argparse
import mmap
import os
import signal
import time


def padreEjecutaHijo1(s, f):
    os.kill(pid1, signal.SIGUSR1)


def padreLee(s, f):
    print("Soy el padre: ", os.getpid())
    area.seek(0)
    leido = area.read(15)
    print("Padre dice: ", leido)
    os.kill(pid2, signal.SIGUSR1)


def hijo1(s, f):
    print("Soy el hijo 1 y estoy trabajando...")
    linea = input("Ingrese una linea por teclado: ")
    if linea == "bye":
        os.kill(os.getppid(), signal.SIGUSR2)
        exit()
    area.seek(0)
    area.write(linea.encode())
    os.kill(os.getppid(), signal.SIGUSR1)
    # signal.pause()


def hijo2(signal, frame):
    print("Soy el hijo 2 y estoy trabajando...")
    area.seek(0)
    leido = area.read(16)
    leido.decode()
    fdw = open(nombreArchivo, 'a')
    fdw.write(str(leido.decode('utf-8').upper())+"\n")
    area.seek(0)


def padreTermina(s, f):
    print("Soy el padre y termino todo: ", os.getpid())
    os.kill(pid2, signal.SIGUSR2)
    os.wait()
    os.wait()
    exit()


def hijo1Exit(signal, frame):
    exit()


def hijo2Exit(signal, frame):
    exit()


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="archivo",
                    required=True, help="Nombre del archivo")
argumento = parser.parse_args()
nombreArchivo = argumento.archivo

area = mmap.mmap(-1, 15)
signal.signal(signal.SIGUSR1, padreLee)
signal.signal(signal.SIGUSR2, padreTermina)

# Crear los procesos hijos
pid1 = os.fork()
if pid1 == 0:
    signal.signal(signal.SIGUSR1, hijo1)
    signal.signal(signal.SIGUSR2, hijo1Exit)
    while True:
        signal.pause()


pid2 = os.fork()
if pid2 == 0:
    signal.signal(signal.SIGUSR1, hijo2)
    signal.signal(signal.SIGUSR2, hijo2Exit)
    while True:
        signal.pause()

time.sleep(1)
# os.kill(pid2, signal.SIGUSR2)
# os.kill(pid1, signal.SIGUSR1)
while True:
    os.kill(pid1, signal.SIGUSR1)
    time.sleep(3)
