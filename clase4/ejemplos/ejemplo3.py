#!/usr/bin/python3

import os
import sys
import time
import subprocess as sp


# Usar Popen y redirreccionar la salida al archivo

output = open("/tmp/output1.txt", "w+")
# con shell True puedo poner todo dentro de las mismas comillas
#cp = sp.Popen(['ls -l /'], shell=True, stdout=output)

cp = sp.Popen(['ls', '-l', '/'], stdout=output)
# esto es equivalente a ls -l  > /tmp/output1.txt
output.close()
