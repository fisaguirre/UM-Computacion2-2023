import mmap
import os
import signal
import time


def padreLee(s, f):
    # signal.signal(signal.SIGUSR1, hijo2)
    print("Estoy vivo3: ", os.getppid(), "- soy: ", os.getpid())
    area.seek(0)
    leido = area.read(16)
    print("Padre dice: ", leido)
    # os.kill(pid2, signal.SIGUSR1)


def hijo1(s, f):
    print("Soy el hijo 1 y estoy trabajando...")
    print(os.getppid(), os.getpid())
    # tarea del hijo 1
    linea = input("Ingrese una linea por teclado: ")
    if linea == "bye":
        exit()
    area.write(linea.encode())
    os.kill(os.getppid(), signal.SIGUSR1)
    signal.pause()


def hijo2(signal, frame):
    print("Soy el hijo 2 y estoy trabajando...")
    # tarea del hijo 2
    time.sleep(5)


area = mmap.mmap(-1, 16)
signal.signal(signal.SIGUSR1, padreLee)
# Crear los procesos hijos
pid1 = os.fork()
if pid1 == 0:
    signal.signal(signal.SIGUSR1, hijo1)
    while True:
        signal.pause()


pid2 = os.fork()
if pid2 == 0:
    signal.signal(signal.SIGUSR2, hijo2)
    while True:
        signal.pause()

# Esperar un poco antes de enviar señales
time.sleep(1)

# Llamar a los procesos hijos
os.kill(pid2, signal.SIGUSR2)
time.sleep(2)
os.kill(pid1, signal.SIGUSR1)

signal.pause()
os.wait()
os.wait()
