import sys
import os
import time
import subprocess as sp
mensaje = input()

sys.stdout.write("\n"+"Soy el hijo 2 - " + str(os.getpid()) +
                 " - mi padre es: " + str(os.getppid())+"\n")
# time.sleep(100)

time.sleep(3)
sys.stdout.write("Mi padre dice: "+mensaje+"\n")
sys.stdout.flush()
