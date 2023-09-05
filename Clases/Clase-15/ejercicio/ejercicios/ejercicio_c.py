"""
2 - Realizar un servidor de mayúsculas que atienda múltiples clientes de forma concurrente utilizando y 
threading utilizando sockets TCP.

El hilo/proceso hijo debe responder con mayúsculas hasta que el cliente envíe la palabra exit. 

En caso de exit el cliente debe administrar correctamente el cierre de la conexión y del proceso/hilo.
"""

#!/usr/bin/python3
import socket, os, threading

def th_server(sock):
    print("Launching thread...")
    while True:
        msg = sock.recv(1024)
        print("Recibido: %s" % msg.decode())
        mensaje = msg.decode().strip()
        if(mensaje == "exit"):
            print("Adios cliente")
            clientsocket.close()
            break
        else:
            print("Recibido: '%s' de %s" % (msg.decode(), addr))
            msg = mensaje.upper()+" \r\n"
            sock.send(msg.encode("ascii"))

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# get local machine name
#host = socket.gethostname()
host = ""
port = 1234

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    msg = 'Thank you for connecting'+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    th = threading.Thread(target=th_server, args=(clientsocket,))
    th.start()