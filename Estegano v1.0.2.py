from PIL import Image #Librería usada para el tratamiento de las imágenes dentro del código
import math  #Utilizado sólo para redondear hacia abajo
import cv2  #Usado únicamente para la conversión a escala de grises

def menu(): #función creada para el menú de opciones.
    correcto = False
    num = 0
    while (not correcto):
        try:#bucle para detectar el número introducido para el menú
            num = int(input())
            correcto = True
        except ValueError: #Creamos una excepción para controlar que únicamente se escriban números enteros
            print('Error, introduce un número entero')

    return num

def opcion1(): #primera función, realizada para ocultar el texto en la imagen

        print("OPCIÓN: Insertar mensaje oculto en una imagen\n")

        caracter_terminacion = [1, 1, 1, 1, 1, 1, 1, 1] #lista inicial de los bits a alterar dentro de la imagen


        def obtener_representacion_ascii(caracter): #funcion para transformar a ASCII
            return ord(caracter)


        def obtener_representacion_binaria(numero):#función para mostrar en binario
            return bin(numero)[2:].zfill(8)


        def cambiar_ultimo_bit(byte, nuevo_bit):#función para seleccionar el último bit
            return byte[:-1] + str(nuevo_bit)


        def binario_a_decimal(binario): #función para transformar de binario a decimal
            return int(binario, 2)


        def modificar_color(color_original, bit):       #en esta función se selecciona el último bit(el menos importante) para modificarle el color
            color_binario = obtener_representacion_binaria(color_original)
            color_modificado = cambiar_ultimo_bit(color_binario, bit)
            return binario_a_decimal(color_modificado)


        def obtener_lista_de_bits(texto): #traduce el texto introducido a bits para poder ser introducidos dentro de la imagen
            lista = []
            for letra in texto:
                representacion_ascii = obtener_representacion_ascii(letra)
                representacion_binaria = obtener_representacion_binaria(representacion_ascii)
                for bit in representacion_binaria:
                    lista.append(bit)
            for bit in caracter_terminacion:
                lista.append(bit)
            return lista

        def ocultar_texto(mensaje, ruta_imagen_original="proyimag1T.png", ruta_imagen_salida="proyimod1T.png"): #en esta función se selecciona la imagen original y el mensaje introducido con su
                                                                                                                    #tradución para introducirlo en la nueva imagen
            imagen = Image.open(ruta_imagen_original)
            pixeles = imagen.load()
            tamaño = imagen.size
            anchura = tamaño[0]
            altura = tamaño[1]
            print("\nProyimag1T.png tiene", anchura, "de ancho y ", altura, "de alto")
            lista = obtener_lista_de_bits(mensaje)
            contador = 0
            longitud = len(lista)
            print("\nOcultando mensaje...".format(mensaje))

            for x in range(anchura):
                for y in range(altura):
                    if contador < longitud:
                        pixel = pixeles[x, y]

                        rojo = pixel[0]
                        verde = pixel[1]
                        azul = pixel[2]
                # se modifican los colores y se establece un contador para asegurar que se introduce el mensaje completo
                        if contador < longitud:
                            rojo_modificado = modificar_color(rojo, lista[contador])
                            contador += 1
                        else:
                            rojo_modificado = rojo

                        if contador < longitud:
                            verde_modificado = modificar_color(verde, lista[contador])
                            contador += 1
                        else:
                            verde_modificado = verde

                        if contador < longitud:
                            azul_modificado = modificar_color(azul, lista[contador])
                            contador += 1
                        else:
                            azul_modificado = azul

                        pixeles[x, y] = (rojo_modificado, verde_modificado, azul_modificado)
                    else:
                        break
                else:
                    continue
                break

            if contador >= longitud:
                print("\nMensaje escrito correctamente")
            else:
                print("\nAdvertencia: no se pudo escribir todo el mensaje, sobraron {} caracteres".format( #en caso de error, muestra este mensaje diciendo cuántos caractéres no se han introducido
                    math.floor((longitud - contador) / 8)))

            imagen.save(ruta_imagen_salida) #se guarda la nueva imagen

            imagen1 = Image.open(ruta_imagen_original)
            imagen2 = Image.open(ruta_imagen_salida)

            if imagen1 != imagen2:  #aquí comprobamos que ambas imágenes son distintas
                print("\nEl fichero proyimag1T.png es diferente a proyimod1T.png")

        texto = input("Introduzca el mensaje de texto a ocultar: ")
        ocultar_texto(texto, "proyimag1T.png")
        imagen = cv2.imread('proyimod1T.png')
        cv2.imshow("Con texto oculto", imagen)  # desde aquí nos muestra la imagen con el texto oculto
        cv2.waitKey(0)


def opcion2(): #función encargada de extraer el mensaje de la imagen

    print("OPCIÓN: Extraer mensaje oculto de una imagen\n")
    print("El fichero de la imagen con texto oculto se llama: proyimod1T.png\n")
    caracter_terminacion = "11111111"

    def obtener_lsb(byte):#explicado anteriormente en la funciíon "opcion1"
        return byte[-1]

    def obtener_representacion_binaria(numero):#explicado anteriormente en la funciíon "opcion1"
        return bin(numero)[2:].zfill(8)

    def binario_a_decimal(binario):#explicado anteriormente en la funciíon "opcion1"
        return int(binario, 2)

    def caracter_desde_codigo_ascii(numero): #explicado anteriormente en la funciíon "opcion1"
        return chr(numero)

    def leer(ruta_imagen):#calcula el altura y anchura de la imagen a usar

        imagen = Image.open(ruta_imagen)
        pixeles = imagen.load()
        tamaño = imagen.size
        anchura = tamaño[0]
        altura = tamaño[1]

        byte = ""
        mensaje = ""


        for x in range(anchura):  #se encarga de "traducir" de binario a codigo ASCII para que sea legible
            for y in range(altura): #con este bucle recuperamos los bits menos importantes para descubrir el mensaje
                pixel = pixeles[x, y]

                rojo = pixel[0]
                verde = pixel[1]
                azul = pixel[2]

                byte += obtener_lsb(obtener_representacion_binaria(rojo))
                if len(byte) >= 8:
                    if byte == caracter_terminacion:
                        break
                    mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                    byte = ""

                byte += obtener_lsb(obtener_representacion_binaria(verde))
                if len(byte) >= 8:
                    if byte == caracter_terminacion:
                        break
                    mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                    byte = ""

                byte += obtener_lsb(obtener_representacion_binaria(azul))
                if len(byte) >= 8:
                    if byte == caracter_terminacion:
                        break
                    mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
                    byte = ""

            else:
                continue
            break
        return mensaje


    mensaje = leer("proyimod1T.png")
    print("Extrayendo el texto de la imagen...\n")
    print("El mensaje oculto es:", mensaje)


def opcion3():

    print("OPCIÓN: Convertir la imagen a escala de grises\n")

    imagen = cv2.imread('proyimod1T.png') #carga la imagen
    print("El fichero de la imagen se llama: proyimag1T.png\n")
    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)#transforma la imagen RGB a escala de grises
    print("Convirtiendo la imagen a escala de grises...")
    cv2.imshow("Escala de grises", img_gris) #muestra por pantalla la imagen ya editada
    cv2.waitKey(0) #Permirte mostrar la imagen manteniendo en pausa el programa hasta que se cierre la ventana.

salir = False
opcion = 0

while not salir:
    print('\n                        Aplicación Estegano\n')
    print("1) Insertar mensaje oculto en una imagen")
    print("2) Extraer mensaje oculto de una imagen")        #menú de opciones del programa principal desde el cual se llaman al resto de funciones
    print("3) Convertir la imagen a escala de grises")
    print("4) Salir")

    print("Opcion: ")

    opcion = menu()

    if opcion == 1:

        opcion1()

    elif opcion == 2:

        opcion2()

    elif opcion == 3:

        opcion3()

    elif opcion == 4:

        salir = True

print("\nCerrando programa...")





