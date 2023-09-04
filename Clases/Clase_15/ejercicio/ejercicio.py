import socket
import multiprocessing

def handle_client(client_socket):
    print("Conexión aceptada desde:", client_socket.getpeername())

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Recibido desde {client_socket.getpeername()}: {data}")

        # Convertir el mensaje a mayúsculas
        response = data.upper()

        # Enviar la respuesta al cliente
        client_socket.send(response.encode('utf-8'))

        if data.strip() == "exit":
            break

    print(f"Conexión cerrada con {client_socket.getpeername()}")
    client_socket.close()

def main():
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 12345       # Puerto en el que escuchará el servidor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Servidor escuchando en {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión entrante de {addr}")

        # Crear un nuevo proceso para manejar al cliente
        client_process = multiprocessing.Process(target=handle_client, args=(client_socket,))
        client_process.start()

if __name__ == "__main__":
    main()
