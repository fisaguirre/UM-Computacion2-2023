import sys
import os
import time
mensaje = input()

sys.stdout.write("\n"+"Soy el hijo 1 - " + str(os.getpid()) +
                 " - mi padre es: " + str(os.getppid())+"\n")
# time.sleep(100)
time.sleep(30)
sys.stdout.write("Mi padre dice: "+mensaje+"\n")
sys.stdout.flush()
