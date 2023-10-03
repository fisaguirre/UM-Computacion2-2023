"""
## EJERCICIOS ##
1 - Implementar un buscador de número primos. Deberá encontrar el número primo inmediátamente inferior a un valor dado.
Debe implementarse utilizando concurrent.futures.

Deberán lanzarse distintos procesos que vayan probando desde 2 hasta el valor dado con pasos 
diferentes para maximizar la posibilidad de encuentro en el menor tiempo.

"""

from __future__ import print_function
from concurrent.futures import ThreadPoolExecutor

def buscarPrimo(numero):
    listaNumeros = []
    
    for i in range(2,numero):
        listaNumeros.append(i)

    for i in listaNumeros:
        if(i%2==0 and i!=2):
            listaNumeros.remove(i)
    
    for i in listaNumeros:
        if(i%3==0 and i!=3):
            listaNumeros.remove(i)
    return listaNumeros.pop()
   

if __name__ == '__main__':
    numeroIngresado = 0
    while True:
        numeroIngresado = int(input("Ingrese un numero mayor o igual a 2: "))
        if (numeroIngresado>=2):
            break
    print(numeroIngresado)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futuro = executor.submit(buscarPrimo, numeroIngresado)
        
        resultado = futuro.result()

        if resultado is not None:
            print("Primero inferior a {0} es: {1}.".format(numeroIngresado, resultado))
        else:
            print("No se encontró ningún número primo inferior a {0}.".format(numeroIngresado))