import io
import os
import time

"""
2 pipes
1 para que escriba el padre y lean los hijos
1 para que escriban los hijos y lea el padre
"""
# Crear pipes
pipe_padre_hijo_r, pipe_padre_hijo_w = os.pipe()
pipe_hijo_padre_r, pipe_hijo_padre_w = os.pipe()

# os.close(pipe_padre_hijo_r)
pipe = os.fdopen(pipe_padre_hijo_w, 'a')
for i in range(5):
    mensaje_padre = "Mensaje del padre "+str(i+1)+"\n"
    pipe.write(mensaje_padre)
    # pipe.flush()
    #os.write(pipe_padre_hijo_w, mensaje_padre.encode())
    # time.sleep(1)
pipe.close()
# os.close(pipe_padre_hijo_w)
print("termina")
for i in range(5):
    print("entra")
    # time.sleep(2)
    pid = os.fork()
    if pid == 0:  # si es un hijo
        # os.close(pipe_padre_hijo_w)
        os.close(pipe_hijo_padre_r)
        while True:
            mensaje_padre = os.read(pipe_padre_hijo_r, 500).decode()
            if (mensaje_padre != ""):
                print("si")

                print(f"Hijo {os.getpid()} recibió: {mensaje_padre}")
                primeraLinea = ""
                for caracter in mensaje_padre:
                    if (caracter != "\n"):
                        primeraLinea = primeraLinea+caracter
                    else:
                        print("texto: ", primeraLinea)
                        mensaje_padre = mensaje_padre.replace(
                            primeraLinea+"\n", "", 1)
                        print("mensaje quedo: ", mensaje_padre)
                        pipe = os.fdopen(pipe_padre_hijo_w, 'w')
                        pipe.write(mensaje_padre)
                        pipe.close()
                        print("sale")
                        break
                print("termina hijo")
                break

        mensaje_hijo = "soy el hijo: "+str(mensaje_padre)
        os.write(pipe_hijo_padre_w, mensaje_hijo.encode())
        # os.close(pipe_padre_hijo_r)
        os.close(pipe_hijo_padre_w)

        os._exit(0)

for i in range(5):
    os.wait()
os.close(pipe_hijo_padre_w)

for i in range(5):
    #pipe = io.open(pipe_hijo_padre_r, 'r')
    #mensaje_hijo = pipe.readline()
    mensaje_hijo = os.read(pipe_hijo_padre_r, 100)
    print(f"Padre {os.getpid()} recibió: {mensaje_hijo}")


os.close(pipe_hijo_padre_r)
