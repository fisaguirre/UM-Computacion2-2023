#!/usr/bin/python3

import os
import sys
import time
import subprocess as sp

# Aca programos esto: ls -l / | grep home | wc -w

# la salida de este proceso la estamos conectando al pipe
# aca estamos creando el pipe
cp_ls = sp.Popen(['ls', '-l', '/'], stdout=sp.PIPE)

# aca estamos diciendo lo que tenga stdout ponelo en stdin y asi conectamos el pipe y quedan conectados os procesos
cp_grep = sp.Popen(["grep", "home"], stdin=cp_ls.stdout, stdout=sp.PIPE)

# una vez que usamos el pipe, y el proceso termina, se muere el pipe
cp_wc = sp.Popen(["wc", "-w"], stdin=cp_grep.stdout)

# tambien podria agregar un script al pipe:
# cp_wc = sp.Popen(["wc", "-w"], stdin=cp_grep.stdout, sp.PIPE)
#cp_script = sp.Popen(["python3", "ejemplo6.py"], stdin=cp_wc.stdout)
