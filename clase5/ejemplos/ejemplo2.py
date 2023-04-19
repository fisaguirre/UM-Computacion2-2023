#!/usr/bin/python3
import os
import time

r, w = os.pipe()

pid = os.fork()

if pid:
    print("I'm processsss: ", os.getpid(), " and my father is: ", os.getppid())
    os.close(w)
    r = os.fdopen(r)
    print('P: leyendo')
    string = r.readline()
    print('P text = ', string)
    os.wait()
    exit()
else:
    print("I'm process: ", os.getpid(), " and my father is: ", os.getppid())
    os.close(r)
    w = os.fdopen(w, 'w')
    print('H: escribiendo ')
    w.write('Texto escrito por el hijo\n')
    w.close()
    print('H: hijo cerrado')
    exit()
