#!/usr/bin/python3

import os
import sys
import time
import subprocess as sp

# Aca programos esto: ls -l / | grep home

# la salida de este proceso la estamos conectando al pipe
# aca estamos creando el pipe
cp_ls = sp.Popen(['ls', '-l', '/'], stdout=sp.PIPE)

# aca estamos diciendo lo que tenga stdout ponelo en stdin y asi conectamos el pipe y quedan conectados os procesos
cp_grep = sp.Popen(["grep", "home"], stdin=cp_ls.stdout)

# una vez que usamos el pipe, y el proceso termina, se muere el pipe
