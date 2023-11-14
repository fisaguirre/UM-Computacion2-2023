Modo de uso:
Correr primero server A y server B, luego cliente.

Cliente:
-i -> ip destino server A
-p -> puerto destino server A
-f -> nombre imagen con extension jpg/jepg
-e (opcional) -> factor de escala para reducir imagen en el server B (reemplaza al factor de escala ingresado en server A)

Ejemplo:
./cliente.py -i 127.0.0.1 -p 8080 -f imagen.jpg
./cliente.py -i 127.0.0.1 -p 8080 -f imagen.jpg -e 3

Server escala grises:
-i -> ip
-p -> puerto escucha
-f -> factor de escala para reducir imagen en server B
-t -> puerto destino server que reduce la imagen

Ejemplo:
./server_gris.py -i 127.0.0.1 -p 8080 -f 2 -t 8081

Server reduce imagen:
-i -> ip server que reduce imagen
-p -> puerto server

Ejemplo:
./server_escalado.py -i 127.0.0.1 -p 8081