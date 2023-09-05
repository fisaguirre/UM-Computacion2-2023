#!/usr/bin/python3
"""
Escribir un programa que implemente un socket pasivo que gestione de forma serializada distintas conecciones entrantes.

Debe atender nuevas conexiones de forma indefinida.

NOTA: cuando decimos serializado decimo que atiende una conexión y 
recibe una nueva conección una vez que esa conexión se cerró
"""

import socket

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
"""
    socket.AF_INET -> sockets tcp/ip
    socket.AF_UNIX -> sockets Unix (archivos en disco, similar a FIFO/named pipes)

    socket.SOCK_STREAM -> socket tcp, orientado a la conexion (flujo de datos)
    socket.SOCK_DGRAM -> socket udp, datagrama de usuario (no orientado a la conexion)
"""

host = "0.0.0.0"
port = 50010

serversocket.bind(('0.0.0.0',50011))                                  

serversocket.listen(1)

while True:
    print("\n")
    print("Esperando conexiones remotas (accept)")
    clientsocket,addr = serversocket.accept()      

    print("Conexión desde %s" % str(addr))
    msg = 'Hola Mundo'+ "\r\n"
    #clientsocket.send(msg.encode('ascii'))
    print("Enviando mensaje...")

    clientsocket.send(msg.encode('utf-8'))
    print("Cerrando conexion...")
    clientsocket.close()
