"""
seguir el ejercicio de la clase y reemplazar el print por otro comando, algo que sea mas de bajo nivel.
"""

import sys
import os
print('PID: %d' % os.getpid())
fh = open('test.txt', 'w')
input('Antes de redireccionar')
sys.stderr = fh
print('Esta línea va a test.txt', file=sys.stderr)
sys.Popen('ccc')
input('Despues de redireccionar')​
sys.stderr = sys.__stderr__
fh.close()
