import sys
import os
import time

mensaje = input()

sys.stdout.write("Soy el hijo 2 - " + str(os.getpid()) +
                 " - mi padre es: " + str(os.getppid())+"\n")
time.sleep(2)

sys.stdout.write("Mi padre dice: "+mensaje+"\n")
sys.stdout.flush()
