import socket

HOST, PORT = "localhost", 5000

def sender():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        while True:
            data = input("Ingrese un mensaje: ")
            if data != 'adios':
                sock.sendto(bytes(data, "utf-8"), (HOST, PORT))
                continue
            break

if __name__ == '__main__':
    sender()