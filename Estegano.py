
import cv2

def menu():
    correcto = False
    num = 0
    while (not correcto):
        try:
            num = int(input())
            correcto = True
        except ValueError:
            print('Error, introduce un numero entero')

    return num


salir = False
opcion = 0

while not salir:
    print('\n                        Aplicación Estegano\n')
    print("1) Insertar mensaje oculto en una imagen")
    print("2) Extraer mensaje oculto de una imagen")
    print("3) Convertir la imagen a escala de grises")
    print("4) Salir")

    print("Opcion: ")

    opcion = menu()

    if opcion == 1:
        opcion1 = ""
    elif opcion == 2:
        opcion2 = ""
    elif opcion == 3:

        imagen = cv2.imread('proyimag1T.png')
        img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        cv2.imshow("color", imagen)
        cv2.imshow("Gris", img_gris)
        cv2.waitKey(0)
        
    elif opcion == 4:

        salir = True

    print("Cerrando programa...")




