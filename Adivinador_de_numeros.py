from random import *

intentos = 0
numero_secreto = randint(1, 100)
nombre = input("Dime tu nombre: ")

print(f"Bueno {nombre}, he pensado un número entre 1 y 100.\nTienes 8 intentos para adivinarlo.")

while intentos < 8:
    estimado = int(input("¿Cuál es el número?: "))
    intentos += 1
    if estimado < numero_secreto:
        print("Mi número es más alto")
    if estimado > numero_secreto:
        print("Mi número es más bajo")
    if estimado == numero_secreto:
        print(f"Felicidades {nombre}! Lo has adivinado en {intentos} intentos.")
        break

if estimado != numero_secreto:
    print(f"Lo siento, se han agotado los intentos. EL número secreto era {numero_secreto}")