#!/usr/bin/python3

import os
import sys
import time
import subprocess as sp


v = sp.run(['ls', '-l', '/'])

print("Tipo v: ", type(v))

print("codigo: ", v.returncode)

print("--------------------------")

# Me va a decir que no existe el file or directory
v2 = sp.run(['ls', '-l', '/f'])

print("Tipo v: ", type(v2))

print("codigo: ", v2.returncode)


# Con capture_output en True, me va a redirigir stdout y stderr
v3 = sp.run(['ls', '-l', '/f'], capture_output=True)

print("Tipo v: ", type(v3))

print("codigo: ", v3.returncode)

print(v3)

print("--------------------------")
# en este no tendrè stderr
v4 = sp.run(['ls', '-l', '/'], capture_output=True)

print("Tipo v: ", type(v4))

print("codigo: ", v4.returncode)

print(v4)

print("-------------------")

# le agregamos el text para que me saque 'b' del stdout
v5 = sp.run(['ls', '-l', '/'], capture_output=True, text=True)

print("Tipo v: ", type(v5))

print("codigo: ", v5.returncode)

print(v5)
