#!/usr/bin/python3

import os
import time

fdr, fdw = os.pipe()

print("PID: ", os.getpid())

# time.slep(20)

pid = os.fork()

if pid == 0:
    os.close(fdw)
    while True:
        leido = os.read(fdr, 2024)
        if len(leido) == 0:
            break

        os.write(1, leido.upper())

    exit()

os.close(fdr)
while True:
    leido = os.read(0, 2024)
    if len(leido) == 0:
        break
    os.write(fdw, leido)
