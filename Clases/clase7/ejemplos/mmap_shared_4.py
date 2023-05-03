import mmap
import os
import signal
import time


def lee(s, f):
    print("Funcion lee")
    leido = area.read(16)
    area.seek(0)
    area.write(leido.decode().upper().encode())
    print("voy a ejecutar otra señal")
    os.kill(pid, signal.SIGUSR1)


def lee_upper(s, f):
    print("FUncion leer upper")
    print(area.read(16))


signal.signal(signal.SIGUSR1, lee)
print("declarada señal 1")
area = mmap.mmap(-1, 16)

pid = os.fork()

if pid == 0:
    print("Hijo")
    signal.signal(signal.SIGUSR1, lee_upper)
    print("declara señal 2")
    area.write(b'soy el hijo')
    os.kill(os.getppid(), signal.SIGUSR1)
    print("ejecutar señal en hijo")
    area.seek(0)
    # time.sleep(2)
    signal.pause()
    exit()

time.sleep(1)
os.wait()
