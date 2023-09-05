"""
2 - Realizar un servidor de mayúsculas que atienda múltiples clientes de forma concurrente utilizando multiprocessing
y utilizando sockets TCP.

El hilo/proceso hijo debe responder con mayúsculas hasta que el cliente envíe la palabra exit. 

En caso de exit el cliente debe administrar correctamente el cierre de la conexión y del proceso/hilo.
"""
#!/usr/bin/python3
import socket, os, multiprocessing, sys

def mp_server(c):
    print("Launching proc...")
    sock,addr = c
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

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 50012

serversocket.bind((host, port))
serversocket.listen(5)

while True:
    cliente = serversocket.accept()

    clientsocket, addr = cliente

    print("Got a connection from %s" % str(addr))

    msg = 'Thank you for connecting'+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    child = multiprocessing.Process(target=mp_server, args=(cliente,))
    child.start()
